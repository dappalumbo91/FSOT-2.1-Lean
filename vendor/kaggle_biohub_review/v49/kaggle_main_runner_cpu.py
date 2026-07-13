#!/usr/bin/env python3
"""
FSOT Kaggle submission — CPU-only (competition runtime has no GPU).

Grading alignment:
  - Output: submission.csv with columns id,dataset,row_type,node_id,t,z,y,x,source_id,target_id
  - Validation: csv_to_geffs round-trip + per-dataset node/edge schema (validate_kaggle_submission.py)
  - Competition score: graph edge Jaccard vs ground truth (train proxy via kaggle_submission_score)

Default engine: fsot + peaks detector (no torch/cuda required).
Set BIOHUB_ENGINE=fsot_unet only when U-Net weights are available; still forces CPU.
"""

from __future__ import annotations

import glob
import os
import sys
from pathlib import Path

# Force CPU before any torch import downstream
os.environ.setdefault("CELLMOT_DEVICE", "cpu")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
os.environ.setdefault("BIOHUB_ENGINE", "fsot")
os.environ.setdefault("BIOHUB_DETECTOR", "peaks")
os.environ.setdefault("CELLMOT_USE_ILP", "0")
os.environ.setdefault("FSOT_LINK_MODE", "fsot_gate")
os.environ.setdefault("FSOT_GATE_FRAC", "0.42")
os.environ.setdefault("FSOT_GAP_LINK", "1")
os.environ.setdefault("KAGGLE_SUBMISSION_FAST_VALIDATE", "0")

LEAN_VERIFICATION_REPO = "https://github.com/dappalumbo91/FSOT-2.1-Lean.git"


def _program_root() -> Path:
    if os.path.exists("/kaggle/working"):
        return Path("/kaggle/working")
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()


PROGRAM_ROOT = _program_root()

if os.path.exists("/kaggle/input"):
    print("[ENV] Kaggle CPU")
    _test_dirs = glob.glob("/kaggle/input/**/test", recursive=True)
    DATA_DIR = _test_dirs[0] if _test_dirs else "/kaggle/input"
    OUT_CSV = "/kaggle/working/submission.csv"
else:
    print("[ENV] Local CPU")
    DATA_DIR = os.environ.get("KAGGLE_TEST_DIR", r"D:\Kaggle_Biohub_Data\test")
    OUT_CSV = str(PROGRAM_ROOT / "submission_cpu.csv")
    _repo = PROGRAM_ROOT / "kaggle-cell-tracking-competition"
    if _repo.exists():
        sys.path.insert(0, str(_repo / "src"))
        sys.path.insert(0, str(_repo / "scripts"))


def _validate_submission_rows(rows: list[dict]) -> None:
    import tempfile

    import pandas as pd
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
            raise ValueError(f"{ds}: node_id must start at 1")
        if int(nd["node_id"].max()) != len(nd):
            raise ValueError(f"{ds}: node_id must be contiguous 1..N")
        node_set = set(nd["node_id"].tolist())
        bad = ed[(~ed["source_id"].isin(node_set)) | (~ed["target_id"].isin(node_set))]
        if len(bad):
            raise ValueError(f"{ds}: {len(bad)} edges reference invalid node_id")


def main() -> None:
    engine = os.environ.get("BIOHUB_ENGINE", "fsot").lower()
    print("=" * 70)
    print("FSOT KAGGLE SUBMISSION — CPU ONLY")
    print(f"Lean ref : {LEAN_VERIFICATION_REPO}")
    print(f"Engine   : {engine}")
    print(f"Device   : {os.environ.get('CELLMOT_DEVICE', 'cpu')}")
    print(f"Data dir : {DATA_DIR}")
    print("=" * 70)

    if not os.path.exists(DATA_DIR):
        print(f"FATAL: missing {DATA_DIR}")
        raise SystemExit(1)

    if engine in ("fsot_unet", "unet"):
        os.environ["CELLMOT_DEVICE"] = "cpu"
        from biohub_unet_engine import graph_to_submission_rows_from_graph, predict_graph

        rows: list[dict] = []
        row_idx = 0
        for ds_name in sorted(d for d in os.listdir(DATA_DIR) if d.endswith(".zarr")):
            clean = ds_name.replace(".zarr", "")
            print(f"[CPU-UNET] {clean}")
            graph = predict_graph(os.path.join(DATA_DIR, clean))
            part, row_idx, _ = graph_to_submission_rows_from_graph(
                graph, clean, row_start=row_idx, node_id_start=1,
            )
            rows.extend(part)
    else:
        from fsot_original_competition import track_all_datasets

        detector = os.environ.get("BIOHUB_DETECTOR", "peaks")
        rows = track_all_datasets(DATA_DIR, detector_mode=detector)

    _validate_submission_rows(rows)
    from biohub_unet_engine import write_submission_csv

    write_submission_csv(rows, Path(OUT_CSV))
    print(f"\n[COMPLETE] {len(rows)} rows -> {OUT_CSV}")
    print("=" * 70)


if __name__ == "__main__":
    main()