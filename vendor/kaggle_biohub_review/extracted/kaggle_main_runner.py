#!/usr/bin/env python3
"""
FSOT KAGGLE COMPETITIVE SUBMISSION
-----------------------------------
Port of the original program: C:\\Users\\damia\\Desktop\\fsot_rna_trinary_evolution_sim

Pipeline (matches kaggle_prototype_fsot_tracker + fsot_full_pipeline_test):
  zarr video → vision detect → FSOT SequenceTracker (fsot_core math) → submission.csv

Engines (BIOHUB_ENGINE):
  fsot       — ORIGINAL PROGRAM: peaks/cellpose detect + FSOT linking (DEFAULT)
  fsot_unet  — U-Net vision gateway + FSOT linking (competition detector upgrade)
  unet       — legacy cellmot transformer edges (not FSOT-first)
  cellpose   — alias for fsot + cellpose detector
  peaks      — alias for fsot + peaks detector

FSOT_LINK_MODE (fsot_unet only): fsot | hybrid | transformer
"""

from __future__ import annotations

import glob
import os
import sys
import zipfile
from pathlib import Path

import pandas as pd

LEAN_VERIFICATION_REPO = "https://github.com/dappalumbo91/FSOT-2.1-Lean.git"


def _program_root() -> Path:
    """Notebook-safe root (Jupyter has no __file__)."""
    if os.path.exists("/kaggle/working"):
        return Path("/kaggle/working")
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()


PROGRAM_ROOT = _program_root()

if os.path.exists("/kaggle/input"):
    print("[ENV] Kaggle")
    _test_dirs = glob.glob("/kaggle/input/**/test", recursive=True)
    DATA_DIR = _test_dirs[0] if _test_dirs else "/kaggle/input"
    OUT_CSV = "/kaggle/working/submission.csv"
    _ft = glob.glob("/kaggle/input/**/cellmot-ft-detector-biohub/**/edge_predictor_best.pth", recursive=True)
    _wt = _ft or glob.glob("/kaggle/input/**/edge_predictor_best.pth", recursive=True)
    if _wt:
        os.environ.setdefault("CELLMOT_UNET_WEIGHTS", _wt[0])
        print(f"[UNET] weights: {_wt[0]}")
    _cp = glob.glob("/kaggle/input/**/cpsam_v2", recursive=True)
    if _cp:
        os.environ.setdefault("CELLPOSE_WEIGHTS", _cp[0])

    def _extract_cellmot_bundle() -> None:
        candidates = glob.glob("/kaggle/input/**/cellmot_code_bundle.zip", recursive=True)
        if os.path.exists("/kaggle/working/cellmot_code_bundle.zip"):
            candidates.insert(0, "/kaggle/working/cellmot_code_bundle.zip")
        for bundle_path in candidates:
            with zipfile.ZipFile(bundle_path, "r") as zf:
                zf.extractall("/kaggle/working")
            sys.path.insert(0, "/kaggle/working/cellmot_bundle/src")
            sys.path.insert(0, "/kaggle/working/cellmot_bundle/scripts")
            print(f"[CELLMOT] bundle extracted from {bundle_path}")
            return
        print("[WARN] cellmot_code_bundle.zip not found — fsot_unet engine unavailable")

    _extract_cellmot_bundle()
    os.environ.setdefault("BIOHUB_ENGINE", "fsot_unet")
    os.environ.setdefault("BIOHUB_DETECTOR", "peaks")
    os.environ.setdefault("FSOT_LINK_MODE", "fsot_gate")
    os.environ.setdefault("FSOT_GATE_FRAC", "0.48")
    os.environ.setdefault("FSOT_GATE_ADAPTIVE", "0")
    os.environ.setdefault("FSOT_GATE_RESCUE", "0")
    os.environ.setdefault("CELLMOT_USE_FT", "1")
    os.environ.setdefault("CELLMOT_DET_THRESHOLD", "0.99")
    os.environ.setdefault("CELLMOT_EDGE_THRESHOLD", "0.3")
    os.environ.setdefault("CELLMOT_USE_ILP", "1")
    os.environ.setdefault("CELLMOT_ILP_MAX_EDGES", "35000")
    os.environ.setdefault("CELLMOT_DET_TTA", "0")
    os.environ.setdefault("CELLMOT_DEVICE", "cpu")
    os.environ.setdefault("CELLMOT_NMS_UM", "8.0")
    os.environ.setdefault("CELLMOT_POOL_UM", "8.0")
    os.environ.setdefault("FSOT_GAP_LINK", "1")
    os.environ.setdefault("KAGGLE_SUBMISSION_FAST_VALIDATE", "1")
else:
    print("[ENV] Local")
    DATA_DIR = r"D:\Kaggle_Biohub_Data\test"
    OUT_CSV = str(PROGRAM_ROOT / "submission_master.csv")
    _repo = PROGRAM_ROOT / "kaggle-cell-tracking-competition"
    if _repo.exists():
        sys.path.insert(0, str(_repo / "src"))
        sys.path.insert(0, str(_repo / "scripts"))

ENGINE = os.environ.get("BIOHUB_ENGINE", "auto").lower()


def _engine_available(name: str) -> bool:
    if name in ("fsot_unet", "unet"):
        try:
            from biohub_unet_engine import _resolve_weights
            _resolve_weights()
            return True
        except Exception:
            return False
    if name == "cellpose":
        try:
            import cellpose  # noqa: F401
            return True
        except Exception:
            return False
    return name in ("fsot", "peaks")


def _pick_engine() -> str:
    if ENGINE != "auto":
        return ENGINE
    # On Kaggle with U-Net weights, default to fsot_unet (matches notebook env).
    if os.path.exists("/kaggle/input") and _engine_available("fsot_unet"):
        return "fsot_unet"
    if os.environ.get("FSOT_PREFER_UNET", "0") == "1" and _engine_available("fsot_unet"):
        return "fsot_unet"
    return "fsot"


def _validate_submission_rows(rows: list[dict]) -> None:
    """Ensure node_id / edge refs reset per dataset (competition sample format)."""
    if os.environ.get("KAGGLE_SUBMISSION_FAST_VALIDATE", "0") != "1":
        import tempfile
        from pathlib import Path

        from biohub_unet_engine import write_submission_csv

        with tempfile.TemporaryDirectory(prefix="biohub_validate_") as tmp:
            csv_path = Path(tmp) / "submission.csv"
            write_submission_csv(rows, csv_path)
            try:
                from validate_kaggle_submission import validate_csv
            except ImportError:
                validate_csv = None
            if validate_csv is not None:
                errors = validate_csv(csv_path, strict_datasets=False)
                if errors:
                    raise ValueError("submission validation failed:\n  " + "\n  ".join(errors))
                return
    df = pd.DataFrame(rows)
    nodes = df[df["row_type"] == "node"]
    edges = df[df["row_type"] == "edge"]
    for ds in nodes["dataset"].unique():
        nd = nodes[nodes["dataset"] == ds]
        ed = edges[edges["dataset"] == ds]
        if int(nd["node_id"].min()) != 1:
            raise ValueError(f"{ds}: node_id must start at 1, got {nd['node_id'].min()}")
        if int(nd["node_id"].max()) != len(nd):
            raise ValueError(f"{ds}: node_id must be contiguous 1..N")
        node_set = set(nd["node_id"].tolist())
        bad = ed[(~ed["source_id"].isin(node_set)) | (~ed["target_id"].isin(node_set))]
        if len(bad):
            raise ValueError(f"{ds}: {len(bad)} edges reference invalid node_id values")


def _run_fsot_unet(data_dir: str, ml_edges: bool) -> list[dict]:
    """U-Net vision gateway (fsot_unet_gateway.py pattern) + FSOT linking."""
    from biohub_unet_engine import graph_to_submission_rows_from_graph, predict_graph

    if ml_edges:
        os.environ.setdefault("FSOT_LINK_MODE", "transformer")
        tag = "UNET-ML"
    else:
        os.environ.setdefault("FSOT_LINK_MODE", "fsot_gate")
        tag = "FSOT-GATE+UNET"

    rows: list[dict] = []
    row_idx = 0
    for ds_name in sorted(d for d in os.listdir(data_dir) if d.endswith(".zarr")):
        clean = ds_name.replace(".zarr", "")
        print(f"[{tag}] {clean}")
        graph = predict_graph(os.path.join(data_dir, clean))
        part, row_idx, _ = graph_to_submission_rows_from_graph(
            graph, clean, row_start=row_idx, node_id_start=1,
        )
        rows.extend(part)
    return rows


def _run_original_fsot(data_dir: str, detector: str) -> list[dict]:
    """Original program port: zarr → detect → FSOT SequenceTracker → rows."""
    from fsot_original_competition import track_all_datasets

    os.environ["BIOHUB_DETECTOR"] = detector
    return track_all_datasets(data_dir, detector_mode=detector)


def main():
    engine = _pick_engine()
    print("=" * 70)
    print("FSOT KAGGLE SUBMISSION — original program port")
    print(f"Program  : {PROGRAM_ROOT}")
    print(f"Lean ref : {LEAN_VERIFICATION_REPO}")
    print(f"Engine   : {engine}")
    print(f"Data dir : {DATA_DIR}")
    print("=" * 70)

    if not os.path.exists(DATA_DIR):
        print(f"FATAL: missing {DATA_DIR}")
        return

    if engine == "fsot_unet":
        rows = _run_fsot_unet(DATA_DIR, ml_edges=False)
    elif engine == "unet":
        rows = _run_fsot_unet(DATA_DIR, ml_edges=True)
    elif engine == "cellpose":
        rows = _run_original_fsot(DATA_DIR, "cellpose")
    elif engine == "peaks":
        rows = _run_original_fsot(DATA_DIR, "peaks")
    else:
        detector = os.environ.get("BIOHUB_DETECTOR", "peaks")
        rows = _run_original_fsot(DATA_DIR, detector)

    _validate_submission_rows(rows)
    from biohub_unet_engine import write_submission_csv

    write_submission_csv(rows, OUT_CSV)
    print(f"\n[COMPLETE] {len(rows)} rows -> {OUT_CSV}")
    print("=" * 70)


if __name__ == "__main__":
    main()