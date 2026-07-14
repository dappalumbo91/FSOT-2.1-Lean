#!/usr/bin/env python3
"""Sweep ILP / det params on train proxy for accuracy toward 0.97."""

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
from biohub_unet_engine import (  # noqa: E402
    graph_to_submission_rows_from_graph,
    predict_graph,
    write_submission_csv,
)
from kaggle_submission_score import score_csv  # noqa: E402

WEIGHTS = Path(r"D:\Kaggle_Biohub_Data\cellmot\cellmot-ft-detector-biohub\edge_predictor_best.pth")
DS = Path(r"D:\Kaggle_Biohub_Data\test\44b6_0113de3b")
GT = Path(r"D:\Kaggle_Biohub_Data\train")

BASE = {
    "CELLMOT_UNET_WEIGHTS": str(WEIGHTS),
    "CELLMOT_DEVICE": "cpu",
    "KAGGLE_CPU_ONLY": "1",
    "FSOT_LINK_MODE": "fsot",
    "FSOT_LIVING_EMERGENCE": "0",
    "FSOT_DET_CONF_RANK": "1",
    "FSOT_GAP_LINK": "1",
    "CELLMOT_USE_ILP": "1",
    "CELLMOT_ILP_MAX_EDGES": "80000",
    "CELLMOT_DET_THRESHOLD": "0.48",
    "CELLMOT_NMS_UM": "6",
}

CONFIGS = [
    ("baseline", {}),
    ("ilp_div3", {"CELLMOT_ILP_DIVISION": "3.0"}),
    ("ilp_div5", {"CELLMOT_ILP_DIVISION": "5.0"}),
    ("ilp_edge_w05", {"CELLMOT_ILP_EDGE_WEIGHT": "-0.5"}),
    ("ilp_app02", {"CELLMOT_ILP_APPEARANCE": "0.02", "CELLMOT_ILP_DISAPPEARANCE": "0.02"}),
    ("det047", {"CELLMOT_DET_THRESHOLD": "0.47"}),
    ("det049", {"CELLMOT_DET_THRESHOLD": "0.49"}),
    ("nms5", {"CELLMOT_NMS_UM": "5"}),
    ("vision_cal", {"FSOT_VISION_CALIBRATE": "1", "CELLMOT_DET_THRESHOLD": ""}),
]


def run_once(name: str, extra: dict[str, str]) -> dict:
    bue._ENGINE_CACHE = None
    for k, v in BASE.items():
        os.environ[k] = v
    for k, v in extra.items():
        if v == "":
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    g = predict_graph(DS)
    rows, _, _ = graph_to_submission_rows_from_graph(g, DS.name.replace(".zarr", ""))
    out = ROOT / f"_tune_ilp_{name}.csv"
    write_submission_csv(rows, out)
    r = score_csv(out, GT)
    out.unlink(missing_ok=True)
    r["nodes"] = g.num_nodes()
    r["edges"] = g.num_edges()
    return r


def main() -> int:
    best = ("", -1.0, {})
    print(f"sweep {len(CONFIGS)} configs on {DS.name}")
    for name, params in CONFIGS:
        try:
            r = run_once(name, params)
            score = r["score"]
            print(
                f"  {name}: score={score:.4f} adj={r['adj_edge_jaccard']:.4f} "
                f"nodes={r['nodes']} edges={r['edges']} params={params}"
            )
            if score > best[1]:
                best = (name, score, params)
        except Exception as exc:
            print(f"  {name}: FAIL {exc}")
    print(f"\nBEST: {best[0]} score={best[1]:.4f} params={best[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())