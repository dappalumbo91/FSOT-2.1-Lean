#!/usr/bin/env python3
"""Fast proxy sweep for v50 competitive hyperparameters (uses cached U-Net engine)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
_REPO = ROOT / "kaggle-cell-tracking-competition"
for p in (_REPO / "src", _REPO / "scripts", ROOT):
    sys.path.insert(0, str(p))

import biohub_unet_engine as bue  # noqa: E402
from biohub_unet_engine import (  # noqa: E402
    graph_to_submission_rows_from_graph,
    predict_graph,
    write_submission_csv,
)
from kaggle_submission_score import score_csv  # noqa: E402


def _run_once(
    ds_path: Path,
    gt_dir: Path,
    out_csv: Path,
    params: dict[str, str],
) -> dict:
    bue._ENGINE_CACHE = None
    for k, v in params.items():
        os.environ[k] = v
    os.environ.setdefault("CELLMOT_UNET_WEIGHTS", str(
        Path(r"D:\Kaggle_Biohub_Data\cellmot\cellmot-ft-detector-biohub\edge_predictor_best.pth")
    ))
    os.environ.setdefault("CELLMOT_DEVICE", "cpu")
    os.environ.setdefault("FSOT_LINK_MODE", "fsot_gate")
    os.environ.setdefault("FSOT_LIVING_EMERGENCE", "0")

    graph = predict_graph(ds_path)
    rows, _, _ = graph_to_submission_rows_from_graph(graph, ds_path.name.replace(".zarr", ""))
    write_submission_csv(rows, out_csv)
    return score_csv(out_csv, gt_dir)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=r"D:\Kaggle_Biohub_Data\test\44b6_0113de3b")
    ap.add_argument("--gt-dir", default=r"D:\Kaggle_Biohub_Data\train")
    ap.add_argument("--max-frames", type=int, default=0, help="0 = full video")
    args = ap.parse_args()

    ds = Path(args.dataset)
    if args.max_frames:
        os.environ["CELLMOT_MAX_FRAMES"] = str(args.max_frames)

    grid = []
    for det in ("0.43", "0.44", "0.45", "0.46", "0.47"):
        for nms in ("5", "6", "7"):
            grid.append({
                "CELLMOT_DET_THRESHOLD": det,
                "CELLMOT_NMS_UM": nms,
                "FSOT_GATE_FRAC": "0.42",
            })
    for gate in ("0.38", "0.46", "0.50"):
        grid.append({
            "CELLMOT_DET_THRESHOLD": "0.45",
            "CELLMOT_NMS_UM": "6",
            "FSOT_GATE_FRAC": gate,
        })

    best = {"score": -1.0, "params": {}}
    print(f"sweep {len(grid)} configs on {ds.name}")
    for i, params in enumerate(grid, 1):
        tag = "_".join(f"{k.split('_')[-1][:3]}{v.replace('.','')}" for k, v in sorted(params.items()))
        out = ROOT / f"tune_{tag}.csv"
        try:
            result = _run_once(ds, Path(args.gt_dir), out, params)
            score = result["score"]
            print(f"[{i}/{len(grid)}] {params} -> {score:.4f}")
            if score > best["score"]:
                best = {"score": score, "params": params, "result": result}
        except Exception as exc:
            print(f"[{i}/{len(grid)}] {params} -> FAIL {exc}")
        if out.exists():
            out.unlink(missing_ok=True)

    print("\nBEST:", best)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())