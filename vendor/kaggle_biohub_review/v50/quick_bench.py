#!/usr/bin/env python3
"""Quick config comparison on train proxy (GPU)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
_REPO = ROOT / "kaggle-cell-tracking-competition"
for p in (_REPO / "src", _REPO / "scripts"):
    sys.path.insert(0, str(p))

import biohub_unet_engine as bue
from biohub_unet_engine import graph_to_submission_rows_from_graph, predict_graph, write_submission_csv
from kaggle_submission_score import score_csv

WEIGHTS = r"D:\Kaggle_Biohub_Data\cellmot\cellmot-ft-detector-biohub\edge_predictor_best.pth"
DS = Path(r"D:\Kaggle_Biohub_Data\test\44b6_0113de3b")
GT = Path(r"D:\Kaggle_Biohub_Data\train")
MAX_FRAMES = os.environ.get("BENCH_MAX_FRAMES", "")


def run_once(name: str, params: dict[str, str]) -> dict:
    bue._ENGINE_CACHE = None
    base = {
        "CELLMOT_UNET_WEIGHTS": WEIGHTS,
        "CELLMOT_DEVICE": "cuda",
        "FSOT_LINK_MODE": "fsot",
        "FSOT_VISION_CALIBRATE": "0",
        "FSOT_LIVING_EMERGENCE": "0",
        "FSOT_DET_CONF_RANK": "1",
    }
    for k, v in {**base, **params}.items():
        os.environ[k] = v
    if MAX_FRAMES:
        os.environ["CELLMOT_MAX_FRAMES"] = MAX_FRAMES
    elif "CELLMOT_MAX_FRAMES" in os.environ:
        del os.environ["CELLMOT_MAX_FRAMES"]

    g = predict_graph(DS)
    rows, _, _ = graph_to_submission_rows_from_graph(g, DS.name.replace(".zarr", ""))
    out = ROOT / f"_bench_{name}.csv"
    write_submission_csv(rows, out)
    r = score_csv(out, GT)
    out.unlink(missing_ok=True)
    r["nodes"] = g.num_nodes()
    r["edges"] = g.num_edges()
    return r


CONFIGS = [
    ("fsot_det044", {"CELLMOT_DET_THRESHOLD": "0.44", "CELLMOT_NMS_UM": "6"}),
    ("fsot_det045", {"CELLMOT_DET_THRESHOLD": "0.45", "CELLMOT_NMS_UM": "6"}),
    ("fsot_det046", {"CELLMOT_DET_THRESHOLD": "0.46", "CELLMOT_NMS_UM": "6"}),
    ("fsot_det047", {"CELLMOT_DET_THRESHOLD": "0.47", "CELLMOT_NMS_UM": "6"}),
    ("fsot_det048", {"CELLMOT_DET_THRESHOLD": "0.48", "CELLMOT_NMS_UM": "6"}),
    ("fsot_det047_nms5", {"CELLMOT_DET_THRESHOLD": "0.47", "CELLMOT_NMS_UM": "5"}),
    ("fsot_det047_nms7", {"CELLMOT_DET_THRESHOLD": "0.47", "CELLMOT_NMS_UM": "7"}),
]


def main() -> int:
    best = ("", -1.0, {})
    print(f"benchmark {len(CONFIGS)} configs on {DS.name} max_frames={MAX_FRAMES or 'full'}")
    for name, params in CONFIGS:
        try:
            r = run_once(name, params)
            print(f"  {name}: score={r['score']:.4f} nodes={r['nodes']} edges={r['edges']}")
            if r["score"] > best[1]:
                best = (name, r["score"], params)
        except Exception as exc:
            print(f"  {name}: FAIL {exc}")
    print(f"\nBEST: {best[0]} score={best[1]:.4f} params={best[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())