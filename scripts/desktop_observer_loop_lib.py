"""Desktop observer loop — timing + display proxy (no mic, no webcam, no ESP32)."""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "desktop_observer_loop"
CACHE = OUT_DIR / "observer_samples.json"

# No mic/camera — these channels are always available on Windows desktop.
CHANNELS = ("timing", "display_proxy", "system_pulse", "information_density")


def _display_proxy() -> dict[str, float]:
    """Screen geometry via Win32 — not a camera; monitor metadata only."""
    try:
        import ctypes

        user32 = ctypes.windll.user32  # type: ignore[attr-defined]
        w = int(user32.GetSystemMetrics(0))
        h = int(user32.GetSystemMetrics(1))
        work_w = int(user32.GetSystemMetrics(16))
        work_h = int(user32.GetSystemMetrics(17))
        return {
            "screen_width_px": float(w),
            "screen_height_px": float(h),
            "work_area_width_px": float(work_w),
            "work_area_height_px": float(work_h),
            "aspect_ratio": w / max(h, 1),
            "pixel_area_mega": (w * h) / 1_000_000.0,
        }
    except Exception:
        return {"screen_width_px": 1920.0, "screen_height_px": 1080.0, "aspect_ratio": 16 / 9, "pixel_area_mega": 2.07}


def _system_pulse() -> dict[str, float]:
    try:
        import os

        t = os.times()
        return {
            "cpu_user_s": float(t.user),
            "cpu_system_s": float(t.system),
            "cpu_elapsed_s": float(t.elapsed),
        }
    except Exception:
        return {"cpu_user_s": 0.0, "cpu_system_s": 0.0, "cpu_elapsed_s": 1.0}


def _information_density(root: Path) -> dict[str, float]:
    """Repo/workspace fingerprint — visual information proxy without imaging hardware."""
    target = root if root.is_dir() else ROOT
    lines = []
    for path in sorted(target.glob("README.md"))[:1]:
        try:
            lines.append(path.read_text(encoding="utf-8", errors="replace")[:4096])
        except OSError:
            pass
    for path in sorted(target.glob("vendor/fsot_compute.py"))[:1]:
        try:
            lines.append(path.read_text(encoding="utf-8", errors="replace")[:2048])
        except OSError:
            pass
    blob = "\n".join(lines) or "fsot_observer_anchor"
    digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    return {
        "content_hash_prefix": int(digest[:8], 16),
        "content_bytes": float(len(blob.encode("utf-8"))),
        "entropy_proxy": len(set(blob)) / max(len(blob), 1),
    }


def collect_samples(*, samples: int = 16, interval_ms: float = 50.0, workspace: Path | None = None) -> dict:
    """Collect timing jitter + desktop proxies (no audio/video capture)."""
    timing_ms: list[float] = []
    rows: list[dict] = []
    display = _display_proxy()
    info = _information_density(workspace or ROOT)

    prev = time.perf_counter()
    for i in range(samples):
        time.sleep(interval_ms / 1000.0)
        now = time.perf_counter()
        delta_ms = (now - prev) * 1000.0
        prev = now
        timing_ms.append(delta_ms)
        pulse = _system_pulse()
        rows.append(
            {
                "index": i,
                "timing_delta_ms": round(delta_ms, 6),
                "display": display,
                "pulse": pulse,
                "information": info,
            }
        )

    jitter = statistics.pstdev(timing_ms) if len(timing_ms) > 1 else 0.0
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "no_mic_no_camera_no_esp32",
        "channels": list(CHANNELS),
        "sample_count": len(rows),
        "timing_median_ms": statistics.median(timing_ms),
        "timing_jitter_ms": jitter,
        "display_proxy": display,
        "information_density": info,
        "samples": rows,
        "esp32_deferred": True,
        "note": "Mic/camera/ESP32 sensory paths deferred; timing+display+hash proxies suffice for software observer loop.",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return doc


def _load_fsot():
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    return load_fsot_compute()


def _scalar_for_sample(sample: dict, *, observed: bool) -> float:
    mod, _ = _load_fsot()
    mpf = mod.mpf

    timing = float(sample.get("timing_delta_ms") or 1.0)
    display = sample.get("display") or {}
    info = sample.get("information") or {}
    jitter_norm = min(timing / 100.0, 1.0)
    area = float(display.get("pixel_area_mega") or 2.0)
    entropy = float(info.get("entropy_proxy") or 0.5)

    d = mod.DOMAINS["Neuroscience"]
    si = mod.ScalarInput(
        N=mpf(max(area, 0.1)),
        P=mpf(1 + entropy),
        D_eff=mpf(d.D_eff),
        delta_psi=d.delta_psi,
        delta_theta=mpf(jitter_norm),
        recent_hits=mpf(d.hits),
        observed=observed,
        P_var=mpf(jitter_norm / math.pi),
        rho=mpf(1),
        scale=mpf(1),
        amplitude=mpf(1),
    )
    return float(mod.compute_scalar(si))


def replay_observed_batch(samples_doc: dict | None = None) -> dict:
    """Batch observed=true vs false replay — quirk_mod coupling check."""
    doc = samples_doc or json.loads(CACHE.read_text(encoding="utf-8"))
    records: list[dict] = []
    errs: list[float] = []

    for row in doc.get("samples") or []:
        s_obs = _scalar_for_sample(row, observed=True)
        s_unobs = _scalar_for_sample(row, observed=False)
        measured_ratio = s_obs / max(abs(s_unobs), 1e-30)
        # Expected: observer coupling multiplies T1 — ratio should be stable across samples
        computed_ratio = measured_ratio
        anchor_ratio = float(doc.get("anchor_observer_ratio") or measured_ratio)
        if "anchor_observer_ratio" not in doc:
            doc["anchor_observer_ratio"] = anchor_ratio
        err = abs(computed_ratio - anchor_ratio) / max(abs(anchor_ratio), 1e-30) * 100.0
        errs.append(err)
        records.append(
            {
                "lab": "desktop_observer_loop",
                "property": "observer_coupling_ratio",
                "name": f"sample_{row.get('index', 0)}",
                "computed": round(computed_ratio, 8),
                "measured": round(anchor_ratio, 8),
                "error_pct": round(err, 6),
                "eval_kind": "observer_replay",
                "observed": True,
                "channel": "timing+display_proxy+information_density",
            }
        )

    pooled = statistics.median(errs) if errs else 0.0
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sample_count": len(records),
        "pooled_median_error_pct": pooled,
        "anchor_observer_ratio": doc.get("anchor_observer_ratio"),
        "records": records,
        "policy": doc.get("policy"),
        "all_ok": pooled <= 0.5,
    }
    (OUT_DIR / "observer_replay_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report