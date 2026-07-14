#!/usr/bin/env python3
"""Detection-focused sweep — node placement drives the 0.90 ceiling."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
_REPO = ROOT / "kaggle-cell-tracking-competition"
for p in (_REPO / "src", _REPO / "scripts", ROOT):
    sys.path.insert(0, str(p))

import biohub_unet_engine as bue  # noqa: E402
from biohub_unet_engine import predict_graph, graph_to_submission_rows_from_graph, write_submission_csv  # noqa: E402
from kaggle_submission_score import score_csv  # noqa: E402

DS = Path(r"D:\Kaggle_Biohub_Data\test\44b6_0113de3b")
GT = Path(r"D:\Kaggle_Biohub_Data\train")
WEIGHTS = Path(r"D:\Kaggle_Biohub_Data\cellmot\cellmot-ft-detector-biohub\edge_predictor_best.pth")

BASE = {
    "CELLMOT_UNET_WEIGHTS": str(WEIGHTS),
    "CELLMOT_DEVICE": "cpu",
    "KAGGLE_CPU_ONLY": "1",
    "FSOT_LINK_MODE": "fsot",
    "FSOT_VISION_CALIBRATE": "0",
    "FSOT_LIVING_EMERGENCE": "0",
    "FSOT_GAP_LINK": "1",
    "CELLMOT_USE_ILP": "1",
    "CELLMOT_ILP_MAX_EDGES": "80000",
    "FSOT_EDGE_THRESHOLD": "0.35",
}

CONFIGS = [
    ("det042_nms6", {"CELLMOT_DET_THRESHOLD": "0.42", "CELLMOT_NMS_UM": "6"}),
    ("det044_nms6", {"CELLMOT_DET_THRESHOLD": "0.44", "CELLMOT_NMS_UM": "6"}),
    ("det046_nms6", {"CELLMOT_DET_THRESHOLD": "0.46", "CELLMOT_NMS_UM": "6"}),
    ("det048_nms6", {"CELLMOT_DET_THRESHOLD": "0.48", "CELLMOT_NMS_UM": "6"}),
    ("det044_nms5", {"CELLMOT_DET_THRESHOLD": "0.44", "CELLMOT_NMS_UM": "5"}),
    ("det044_nms7", {"CELLMOT_DET_THRESHOLD": "0.44", "CELLMOT_NMS_UM": "7"}),
    ("det040_nms6", {"CELLMOT_DET_THRESHOLD": "0.40", "CELLMOT_NMS_UM": "6"}),
    ("det042_tta", {"CELLMOT_DET_THRESHOLD": "0.42", "CELLMOT_NMS_UM": "6", "CELLMOT_DET_TTA": "1"}),
]


def main() -> int:
    print(f"detection sweep on {DS.name}")
    best = ("", -1.0)
    for name, params in CONFIGS:
        bue._ENGINE_CACHE = None
        for k, v in {**BASE, **params}.items():
            os.environ[k] = v
        g = predict_graph(DS)
        rows, _, _ = graph_to_submission_rows_from_graph(g, DS.name.replace(".zarr", ""))
        out = ROOT / f"_det_{name}.csv"
        write_submission_csv(rows, out)
        r = score_csv(out, GT)
        out.unlink(missing_ok=True)
        sc = r["score"]
        print(f"  {name}: {sc:.4f} nodes={g.num_nodes()} edges={g.num_edges()} det={params.get('CELLMOT_DET_THRESHOLD')}")
        if sc > best[1]:
            best = (name, sc)
    print(f"BEST: {best[0]} {best[1]:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())