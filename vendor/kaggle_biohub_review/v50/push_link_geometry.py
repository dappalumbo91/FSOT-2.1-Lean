#!/usr/bin/env python3
"""FSOT linking geometry sweep — targets the 5 edge errors (3 FP + 2 FN) on train GT."""

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
    "FSOT_LINK_MODE": "fsot",
    "FSOT_VISION_CALIBRATE": "1",
    "FSOT_LIVING_EMERGENCE": "0",
    "FSOT_GAP_LINK": "1",
    "CELLMOT_USE_ILP": "1",
    "CELLMOT_ILP_MAX_EDGES": "80000",
    "CELLMOT_NMS_UM": "6",
    "FSOT_EDGE_THRESHOLD": "0.35",
}

CONFIGS = [
    ("base", {}),
    ("trans20", {"FSOT_TRANSLATION_MAX_UM": "20"}),
    ("trans30", {"FSOT_TRANSLATION_MAX_UM": "30"}),
    ("trans35", {"FSOT_TRANSLATION_MAX_UM": "35"}),
    ("gap4", {"FSOT_GAP_MAX": "4"}),
    ("gap5", {"FSOT_GAP_MAX": "5"}),
    ("gap_scale12", {"FSOT_GAP_DISTANCE_SCALE": "1.2"}),
    ("gap_scale15", {"FSOT_GAP_DISTANCE_SCALE": "1.5"}),
    ("no_ilp", {"CELLMOT_USE_ILP": "0"}),
    ("edge028", {"FSOT_EDGE_THRESHOLD": "0.28"}),
    ("edge032", {"FSOT_EDGE_THRESHOLD": "0.32"}),
]


def main() -> int:
    print("link geometry sweep")
    best = ("", -1.0, 0, 0, 0)
    for name, params in CONFIGS:
        bue._ENGINE_CACHE = None
        for k, v in {**BASE, **params}.items():
            os.environ[k] = v
        g = predict_graph(DS)
        rows, _, _ = graph_to_submission_rows_from_graph(g, DS.name.replace(".zarr", ""))
        out = ROOT / f"_geom_{name}.csv"
        write_submission_csv(rows, out)
        r = score_csv(out, GT)
        out.unlink(missing_ok=True)
        sc = r["score"]
        print(f"  {name}: {sc:.4f} nodes={g.num_nodes()} edges={g.num_edges()}")
        if sc > best[1]:
            best = (name, sc, g.num_nodes(), g.num_edges(), 0)
    print(f"BEST: {best[0]} {best[1]:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())