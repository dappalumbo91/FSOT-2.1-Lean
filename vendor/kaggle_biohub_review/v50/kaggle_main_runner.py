#!/usr/bin/env python3
"""
FSOT Kaggle v50 — competitive U-Net detection + FSOT vision/linking.

Pipeline:
  zarr → [U-Net detect + conf-ranked NMS] → centroids
       → [FSOT SequenceTracker linking] → submission.csv

Engines (BIOHUB_ENGINE):
  fsot_unet  — U-Net + FSOT gate linking (DEFAULT when weights available)
  fsot       — peaks/cellpose detect + FSOT linking (fast CPU fallback)
  auto       — fsot_unet if weights found, else fsot

Kaggle: attach cellmot-ft-detector-biohub + cellmot-baseline-artifacts.
Local: set CELLMOT_UNET_WEIGHTS or place weights under cellmot_weights/.
"""

from __future__ import annotations

import glob
import os
import sys
import zipfile
from pathlib import Path

LEAN_VERIFICATION_REPO = "https://github.com/dappalumbo91/FSOT-2.1-Lean.git"


def _program_root() -> Path:
    if os.path.exists("/kaggle/working"):
        return Path("/kaggle/working")
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()


PROGRAM_ROOT = _program_root()


def _setup_kaggle_env() -> tuple[str, str]:
    _test_dirs = glob.glob("/kaggle/input/**/test", recursive=True)
    data_dir = _test_dirs[0] if _test_dirs else "/kaggle/input"
    out_csv = "/kaggle/working/submission.csv"

    _ft = glob.glob("/kaggle/input/**/cellmot-ft-detector-biohub/**/edge_predictor_best.pth", recursive=True)
    _wt = _ft or glob.glob("/kaggle/input/**/edge_predictor_best.pth", recursive=True)
    if _wt:
        os.environ.setdefault("CELLMOT_UNET_WEIGHTS", _wt[0])
        print(f"[UNET] weights: {_wt[0]}")

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
        print("[WARN] cellmot_code_bundle.zip not found — pip install tracksdata/cellmot from wheels")

    _extract_cellmot_bundle()

    # v50 defaults: U-Net FT detect + FSOT pure link + ILP consistency
    os.environ.setdefault("BIOHUB_ENGINE", "auto")
    os.environ.setdefault("FSOT_VISION_CALIBRATE", "1")
    os.environ.setdefault("FSOT_LIVING_EMERGENCE", "1")
    os.environ.setdefault("FSOT_LIVING_ADAPTIVE", "1")
    os.environ.setdefault("FSOT_DET_CONF_RANK", "1")
    os.environ.setdefault("FSOT_LIVING_PROXY_ACCURACY", "0.90")
    os.environ.setdefault("FSOT_LIVING_MIN_UNET_CONF", "0.0")
    os.environ.setdefault("FSOT_LIVING_TARGET_PER_FRAME", "258")
    os.environ.setdefault("FSOT_LINK_MODE", "fsot")
    os.environ.setdefault("FSOT_GATE_FRAC", "0.42")
    os.environ.setdefault("FSOT_GATE_ADAPTIVE", "1")
    os.environ.setdefault("FSOT_GATE_RESCUE", "1")
    os.environ.setdefault("CELLMOT_USE_FT", "1")
    os.environ.setdefault("CELLMOT_DET_THRESHOLD", "0.48")
    os.environ.setdefault("CELLMOT_EDGE_THRESHOLD", "0.25")
    os.environ.setdefault("CELLMOT_USE_ILP", "1")
    os.environ.setdefault("CELLMOT_ILP_MAX_EDGES", "80000")
    os.environ.setdefault("CELLMOT_DET_TTA", "0")
    os.environ.setdefault("CELLMOT_NMS_UM", "6.0")
    os.environ.setdefault("CELLMOT_POOL_UM", "8.0")
    os.environ.setdefault("FSOT_GAP_LINK", "1")
    os.environ.setdefault("KAGGLE_SUBMISSION_FAST_VALIDATE", "0")

    # Use GPU when Kaggle assigns one; CPU fallback is automatic in biohub_unet_engine
    if os.environ.get("CUDA_VISIBLE_DEVICES", "") != "":
        os.environ.setdefault("CELLMOT_DEVICE", "cuda")
    else:
        os.environ.setdefault("CELLMOT_DEVICE", "cuda" if _gpu_available() else "cpu")

    return data_dir, out_csv


def _gpu_available() -> bool:
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:
        return False


def _setup_local_env() -> tuple[str, str]:
    data_dir = os.environ.get("KAGGLE_TEST_DIR", r"D:\Kaggle_Biohub_Data\test")
    out_csv = str(PROGRAM_ROOT / "submission_v50.csv")

    _repo = PROGRAM_ROOT / "kaggle-cell-tracking-competition"
    if _repo.exists():
        sys.path.insert(0, str(_repo / "src"))
        sys.path.insert(0, str(_repo / "scripts"))

    # Local weight discovery
    if not os.environ.get("CELLMOT_UNET_WEIGHTS"):
        for candidate in (
            Path(r"D:\Kaggle_Biohub_Data\cellmot\cellmot-ft-detector-biohub\edge_predictor_best.pth"),
            PROGRAM_ROOT / "cellmot_weights/cellmot-ft-detector-biohub/edge_predictor_best.pth",
            Path(r"D:\Kaggle_Biohub_Data\cellmot\cellmot-baseline-artifacts\weights\unet_transformer\split_0\edge_predictor_best.pth"),
        ):
            if candidate.exists():
                os.environ["CELLMOT_UNET_WEIGHTS"] = str(candidate)
                print(f"[UNET] local weights: {candidate}")
                break

    os.environ.setdefault("BIOHUB_ENGINE", "auto")
    os.environ.setdefault("FSOT_VISION_CALIBRATE", "1")
    os.environ.setdefault("FSOT_LIVING_EMERGENCE", "1")
    os.environ.setdefault("FSOT_LIVING_ADAPTIVE", "1")
    os.environ.setdefault("FSOT_DET_CONF_RANK", "1")
    os.environ.setdefault("FSOT_LIVING_PROXY_ACCURACY", "0.90")
    os.environ.setdefault("FSOT_LIVING_MIN_UNET_CONF", "0.0")
    os.environ.setdefault("FSOT_LIVING_TARGET_PER_FRAME", "258")
    os.environ.setdefault("FSOT_LINK_MODE", "fsot")
    os.environ.setdefault("FSOT_GATE_FRAC", "0.42")
    os.environ.setdefault("FSOT_GATE_ADAPTIVE", "1")
    os.environ.setdefault("FSOT_GATE_RESCUE", "1")
    os.environ.setdefault("CELLMOT_USE_ILP", "1")
    os.environ.setdefault("CELLMOT_ILP_MAX_EDGES", "80000")
    os.environ.setdefault("CELLMOT_DET_THRESHOLD", "0.48")
    os.environ.setdefault("CELLMOT_NMS_UM", "6.0")
    os.environ.setdefault("CELLMOT_DEVICE", "cuda" if _gpu_available() else "cpu")
    os.environ.setdefault("KAGGLE_SUBMISSION_FAST_VALIDATE", "0")
    return data_dir, out_csv


if os.path.exists("/kaggle/input"):
    print("[ENV] Kaggle")
    DATA_DIR, OUT_CSV = _setup_kaggle_env()
else:
    print("[ENV] Local")
    DATA_DIR, OUT_CSV = _setup_local_env()


def _engine_available(name: str) -> bool:
    if name in ("fsot_unet", "unet"):
        try:
            from biohub_unet_engine import _resolve_weights
            _resolve_weights()
            return True
        except Exception as exc:
            print(f"[WARN] fsot_unet unavailable: {exc}")
            return False
    return name in ("fsot", "peaks", "cellpose")


def _pick_engine() -> str:
    requested = os.environ.get("BIOHUB_ENGINE", "auto").lower()
    if requested != "auto":
        return requested
    if _engine_available("fsot_unet"):
        return "fsot_unet"
    return "fsot"


def _validate_submission_rows(rows: list[dict]) -> None:
    import tempfile

    import pandas as pd

    try:
        from submission_io import write_submission_csv
    except ImportError:
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


def _max_frames() -> int | None:
    raw = os.environ.get("CELLMOT_MAX_FRAMES", "").strip()
    if not raw:
        return None
    return int(raw)


def _run_fsot_unet(data_dir: str) -> list[dict]:
    from biohub_unet_engine import graph_to_submission_rows_from_graph, predict_graph

    max_t = _max_frames()
    rows: list[dict] = []
    row_idx = 0
    for ds_name in sorted(d for d in os.listdir(data_dir) if d.endswith(".zarr")):
        clean = ds_name.replace(".zarr", "")
        print(f"[FSOT-UNET] {clean}" + (f" (max_frames={max_t})" if max_t else ""))
        graph = predict_graph(os.path.join(data_dir, clean), max_frames=max_t)
        part, row_idx, _ = graph_to_submission_rows_from_graph(
            graph, clean, row_start=row_idx, node_id_start=1,
        )
        rows.extend(part)
    return rows


def _run_original_fsot(data_dir: str, detector: str) -> list[dict]:
    from fsot_original_competition import track_all_datasets

    return track_all_datasets(data_dir, detector_mode=detector)


def main() -> None:
    engine = _pick_engine()
    print("=" * 70)
    print("FSOT KAGGLE v50 — U-Net + FSOT vision/linking")
    print(f"Lean ref : {LEAN_VERIFICATION_REPO}")
    print(f"Engine   : {engine}")
    print(f"Link     : {os.environ.get('FSOT_LINK_MODE', 'fsot_gate')}")
    print(f"Vision   : FSOT_VISION_CALIBRATE={os.environ.get('FSOT_VISION_CALIBRATE', '1')}")
    print(f"Device   : {os.environ.get('CELLMOT_DEVICE', 'cpu')}")
    print(f"Data dir : {DATA_DIR}")
    print("=" * 70)

    if not os.path.exists(DATA_DIR):
        print(f"FATAL: missing {DATA_DIR}")
        raise SystemExit(1)

    if engine in ("fsot_unet", "unet"):
        rows = _run_fsot_unet(DATA_DIR)
    else:
        detector = os.environ.get("BIOHUB_DETECTOR", "peaks")
        rows = _run_original_fsot(DATA_DIR, detector)

    _validate_submission_rows(rows)
    try:
        from submission_io import write_submission_csv
    except ImportError:
        from biohub_unet_engine import write_submission_csv

    write_submission_csv(rows, Path(OUT_CSV))
    print(f"\n[COMPLETE] {len(rows)} rows -> {OUT_CSV}")
    print("=" * 70)


if __name__ == "__main__":
    main()