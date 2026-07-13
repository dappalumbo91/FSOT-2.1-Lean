#!/usr/bin/env python3
"""
FSOT vision calibration — map zarr image statistics to U-Net detection threshold.

Applies the same scalar engine used for linking (fsot_core.compute_scalar_biological)
to the *detection* stage: coherent signal (low delta_psi) → lower det_threshold for
recall; noisy/sparse signal → higher threshold to suppress false positives.

Set FSOT_VISION_CALIBRATE=1 (default in v50) to enable per-dataset threshold tuning.
Override with CELLMOT_DET_THRESHOLD when you want a fixed value.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

from fsot_core import FERTILE_HIGH, FERTILE_LOW, K, compute_scalar_biological


def _read_quantiles(ds_path: Path) -> tuple[float, float, float]:
    """Return (q_low, q_high, dynamic_range) from zarr attrs or a quick sample."""
    import zarr

    zg = zarr.open_group(str(ds_path), mode="r")
    attrs = dict(zg.attrs)
    stats = attrs.get("image_statistics") or attrs.get("metadata", {}).get("image_statistics", {})
    if isinstance(stats, str):
        stats = json.loads(stats)
    quantiles = stats.get("quantiles") or {}
    q_low = float(quantiles.get("0.001", quantiles.get("0.01", 0.0)))
    q_high = float(quantiles.get("0.999", quantiles.get("0.99", 1.0)))
    if q_high > q_low:
        return q_low, q_high, q_high - q_low

    arr = zg["0"]
    sample = np.asarray(arr[0, ::8, ::8, ::8], dtype=np.float32)
    q_low, q_high = np.percentile(sample, [0.1, 99.9])
    return float(q_low), float(q_high), float(q_high - q_low)


def _frame_density_proxy(ds_path: Path, downsample: int = 8) -> float:
    """Fraction of voxels above adaptive foreground level (mitosis/cell density proxy)."""
    import zarr

    zg = zarr.open_group(str(ds_path), mode="r")
    arr = zg["0"]
    t_max = min(3, arr.shape[0])
    chunks = []
    for t in range(t_max):
        sl = arr[t, ::downsample, ::downsample, ::downsample]
        chunks.append(np.asarray(sl, dtype=np.float32))
    stack = np.concatenate([c.ravel() for c in chunks])
    med = float(np.median(stack))
    mad = float(np.median(np.abs(stack - med))) + 1e-6
    fg = stack > med + 2.5 * mad
    return float(fg.mean())


def fsot_detection_threshold(
    ds_path: str | Path,
    *,
    base: float = 0.55,
    lo: float = 0.45,
    hi: float = 0.68,
) -> tuple[float, dict]:
    """
    Derive U-Net det_threshold from FSOT scalar on vision observables.

    Returns (threshold, diagnostics).
    """
    ds_path = Path(ds_path)
    if not ds_path.exists() and ds_path.suffix != ".zarr":
        alt = Path(str(ds_path) + ".zarr")
        if alt.exists():
            ds_path = alt
    if ds_path.suffix in (".zarr", ".geff"):
        zarr_root = ds_path if ds_path.suffix == ".zarr" else ds_path.parent / (ds_path.stem + ".zarr")
        if zarr_root.exists():
            ds_path = zarr_root
        else:
            ds_path = ds_path.parent / ds_path.stem

    q_low, q_high, dyn = _read_quantiles(ds_path)
    density = _frame_density_proxy(ds_path)

    # delta_psi analog: inverse signal coherence (wider quantile span → noisier → higher psi)
    span_norm = min(max(dyn / max(q_high, 1.0), 0.02), 0.35)
    delta_psi = 0.04 + 0.22 * span_norm + 0.12 * (1.0 - min(density * 8.0, 1.0))

    n_obs = 0.5 + 0.5 * min(density * 6.0, 1.0)
    s = compute_scalar_biological(N=n_obs, P=1.0, delta_psi=delta_psi, amplitude=1.0)

    # Fertile-window proximity → recall-friendly threshold adjustment
    mid = 0.5 * (FERTILE_LOW + FERTILE_HIGH)
    fertile_dist = abs(s - mid) / max(mid, 1e-6)
    k_pull = min(max((s / K) if K > 0 else 1.0, 0.35), 1.65)

    # Lower threshold when scalar sits in fertile band (more true cells to recover)
    adjust = 0.08 * (fertile_dist - 0.5) - 0.05 * (k_pull - 1.0)
    thr = base + adjust
    thr = min(max(thr, lo), hi)

    diag = {
        "dataset": ds_path.name,
        "q_low": q_low,
        "q_high": q_high,
        "dynamic_range": dyn,
        "density_proxy": density,
        "delta_psi": delta_psi,
        "n_obs": n_obs,
        "scalar_s": s,
        "fertile_dist": fertile_dist,
        "k_pull": k_pull,
        "det_threshold": thr,
    }
    return thr, diag


def apply_fsot_vision_calibrate(ds_path: str | Path) -> float:
    """Env-gated wrapper used by biohub_unet_engine before inference."""
    if os.environ.get("FSOT_VISION_CALIBRATE", "1") != "1":
        return float(os.environ.get("CELLMOT_DET_THRESHOLD", "0.55"))
    if os.environ.get("CELLMOT_DET_THRESHOLD"):
        return float(os.environ["CELLMOT_DET_THRESHOLD"])
    base = float(os.environ.get("FSOT_VISION_BASE_THRESHOLD", "0.55"))
    lo = float(os.environ.get("FSOT_VISION_THRESHOLD_LO", "0.45"))
    hi = float(os.environ.get("FSOT_VISION_THRESHOLD_HI", "0.68"))
    thr, diag = fsot_detection_threshold(ds_path, base=base, lo=lo, hi=hi)
    if os.environ.get("FSOT_LIVING_EMERGENCE", "0") == "1":
        try:
            from fsot_living_emergence import apply_living_det_adjustments, living_vision_state

            proxy = float(os.environ.get("FSOT_LIVING_PROXY_ACCURACY", "0.90"))
            state = living_vision_state(
                proxy_accuracy=proxy,
                mean_brightness=min(max(diag["density_proxy"] * 4.0, 0.2), 0.8),
            )
            thr = apply_living_det_adjustments(thr, state)
            print(
                f"[FSOT-LIVING] regime={state.regime} det_adj={state.det_threshold_delta:+.3f} "
                f"→ det_thr={thr:.3f}"
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] FSOT-Living det adjust skipped: {exc}")
    print(
        f"[FSOT-VISION] {diag['dataset']} S={diag['scalar_s']:.4f} "
        f"Δψ={diag['delta_psi']:.3f} det_thr={thr:.3f}"
    )
    return thr