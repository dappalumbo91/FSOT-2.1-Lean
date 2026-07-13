#!/usr/bin/env python3
"""
FSOT Original Program → Kaggle Competition Port
================================================
Maps the pre-competition codebase (fsot_rna_trinary_evolution_sim) to Biohub submission.

Original program chain (same repo, files-7ed1e62c):
  zarr_ingestion_pipeline.py     Load OME-Zarr (T,Z,Y,X)
  fsot_full_pipeline_test.py     SciPy/threshold vision proxy + fsot_tracking_engine
  fsot_mitosis_predictor.py      Phase-scalar S mitosis gates
  fsot_3d_vision_network.py      FSOT-NN PhaseGate detector (future native vision)
  fsot_unet_gateway.py           Vision centroids → FSOT lineage resolver
  fsot_cellular_bridge.py        Production tracker: link_cost + mitosis_ready (fsot_core)
  kaggle_prototype_fsot_tracker.py  submission.csv node/edge format

Competition port (this module):
  detect  → CompetitiveDetector (peaks/cellpose) OR U-Net coords (gateway mode)
  link    → fsot_cellular_bridge.SequenceTracker (100% FSOT scalar math)
  export  → per-dataset node_id reset + validation
"""

from __future__ import annotations

import os
from pathlib import Path

import dask.array as da
import zarr

from biohub_competitive import CompetitiveDetector, DatasetContext
from fsot_cellular_bridge import SequenceTracker
from fsot_core import COLLAPSE_THRESHOLD, compute_scalar_biological

ROOT = Path(__file__).resolve().parent
ORIGIN = "fsot_rna_trinary_evolution_sim/files-7ed1e62c"


def verify_fsot_core() -> None:
    """Prove fsot_core scalar engine is live before tracking."""
    s = compute_scalar_biological(delta_psi=0.35, observed=True)
    print(f"[FSOT-CORE] biological scalar S={s:.6f}  collapse_threshold={COLLAPSE_THRESHOLD:.4f}")
    print(f"[FSOT-CORE] Lean ref: github.com/dappalumbo91/FSOT-2.1-Lean")
    print(f"[FSOT-CORE] origin: {ORIGIN}")


def _open_video(zarr_path: str | Path) -> tuple[da.Array, DatasetContext]:
    """Load lazy video array + quantile context (zarr_ingestion_pipeline pattern)."""
    zarr_path = Path(zarr_path)
    store = zarr_path if zarr_path.suffix == ".zarr" else zarr_path.parent / f"{zarr_path.name}.zarr"
    try:
        attrs = dict(zarr.open_group(str(store), mode="r").attrs)
        ctx = DatasetContext(
            quantiles=attrs.get("image_statistics", {}).get("quantiles", {}),
        )
    except Exception:  # noqa: BLE001
        ctx = DatasetContext()
    video = da.from_zarr(zarr.open(str(store), mode="r")["0"])
    if video.ndim == 5:
        video = video[:, 0, :, :, :]
    return video, ctx


def track_dataset_native(
    zarr_path: str | Path,
    dataset_name: str,
    detector_mode: str | None = None,
    row_start: int = 0,
) -> tuple[list[dict], int]:
    """
    Original FSOT program port: vision detect → SequenceTracker → submission rows.

    Evolves fsot_full_pipeline_test.fsot_tracking_engine into full-video
    fsot_cellular_bridge.SequenceTracker with competition quantile peaks/cellpose.
    """
    mode = detector_mode or os.environ.get("BIOHUB_DETECTOR", "peaks")
    det = CompetitiveDetector(mode=mode)
    video, ctx = _open_video(zarr_path)
    det.ctx = ctx

    rows: list[dict] = []
    row_idx = row_start
    node_id = 1
    tracker = SequenceTracker()
    prev_edges = 0

    print(f"[FSOT-NATIVE] {dataset_name} detector={mode} frames={video.shape[0]}")
    for t in range(video.shape[0]):
        cells = det(video[t].compute())
        gids: list[int] = []
        for c in cells:
            gids.append(node_id)
            rows.append({
                "id": row_idx, "dataset": dataset_name, "row_type": "node",
                "node_id": node_id, "t": t,
                "z": int(round(c["z"])), "y": int(round(c["y"])), "x": int(round(c["x"])),
                "source_id": -1, "target_id": -1,
            })
            row_idx += 1
            node_id += 1
        tracker.advance(t, cells, gids)
        for src, tgt in tracker.edges[prev_edges:]:
            rows.append({
                "id": row_idx, "dataset": dataset_name, "row_type": "edge",
                "node_id": -1, "t": -1, "z": -1, "y": -1, "x": -1,
                "source_id": src, "target_id": tgt,
            })
            row_idx += 1
        prev_edges = len(tracker.edges)

    print(f"[FSOT-NATIVE] {dataset_name} nodes={node_id - 1} edges={len(tracker.edges)}")
    print(det.stats.summary())
    return rows, row_idx


def track_all_datasets(
    data_dir: str | Path,
    detector_mode: str | None = None,
) -> list[dict]:
    """Run native FSOT port on every .zarr in a competition data directory."""
    verify_fsot_core()
    data_dir = Path(data_dir)
    rows: list[dict] = []
    row_idx = 0
    for ds_name in sorted(d for d in os.listdir(data_dir) if d.endswith(".zarr")):
        clean = ds_name.replace(".zarr", "")
        part, row_idx = track_dataset_native(
            data_dir / ds_name, clean, detector_mode=detector_mode, row_start=row_idx,
        )
        rows.extend(part)
    return rows