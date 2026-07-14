#!/usr/bin/env python3
"""Aggressive link-mode sweep — target closing gap to leaderboard ~0.97."""

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
    "FSOT_VISION_CALIBRATE": "1",
    "FSOT_LIVING_EMERGENCE": "0",
    "FSOT_DET_CONF_RANK": "1",
    "FSOT_GAP_LINK": "1",
    "CELLMOT_USE_ILP": "1",
    "CELLMOT_ILP_MAX_EDGES": "80000",
    "CELLMOT_DET_THRESHOLD": "0.48",
    "CELLMOT_NMS_UM": "6",
    "CELLMOT_EDGE_THRESHOLD": "0.25",
}

CONFIGS: list[tuple[str, dict[str, str]]] = [
    ("fsot_pure", {"FSOT_LINK_MODE": "fsot"}),
    ("transformer_ilp", {"FSOT_LINK_MODE": "transformer"}),
    ("hybrid_ilp", {"FSOT_LINK_MODE": "hybrid"}),
    ("fsot_union", {"FSOT_LINK_MODE": "fsot_union"}),
    ("gate_soft_rescue", {
        "FSOT_LINK_MODE": "fsot_gate",
        "FSOT_GATE_SOFT": "1",
        "FSOT_GATE_RESCUE": "1",
        "FSOT_GATE_FRAC": "0.35",
    }),
    ("gate_soft_low", {
        "FSOT_LINK_MODE": "fsot_gate",
        "FSOT_GATE_SOFT": "1",
        "FSOT_GATE_RESCUE": "1",
        "FSOT_GATE_FRAC": "0.28",
        "FSOT_GATE_ML_KEEP": "0.25",
    }),
    ("transformer_edge02", {
        "FSOT_LINK_MODE": "transformer",
        "CELLMOT_EDGE_THRESHOLD": "0.20",
    }),
    ("transformer_edge15", {
        "FSOT_LINK_MODE": "transformer",
        "CELLMOT_EDGE_THRESHOLD": "0.15",
    }),
    ("union_edge02", {
        "FSOT_LINK_MODE": "fsot_union",
        "CELLMOT_EDGE_THRESHOLD": "0.20",
    }),
]


def run_once(name: str, extra: dict[str, str]) -> dict:
    bue._ENGINE_CACHE = None
    for k, v in {**BASE, **extra}.items():
        os.environ[k] = v
    g = predict_graph(DS)
    rows, _, _ = graph_to_submission_rows_from_graph(g, DS.name.replace(".zarr", ""))
    out = ROOT / f"_push_{name}.csv"
    write_submission_csv(rows, out)
    r = score_csv(out, GT)
    out.unlink(missing_ok=True)
    r["nodes"] = g.num_nodes()
    r["edges"] = g.num_edges()
    r["name"] = name
    return r


def main() -> int:
    target = 0.97
    print(f"push_accuracy on {DS.name} — target {target:.2f}, current best ~0.904")
    results: list[dict] = []
    for name, params in CONFIGS:
        try:
            r = run_once(name, params)
            results.append(r)
            print(
                f"  {name}: score={r['score']:.4f} adj={r['adj_edge_jaccard']:.4f} "
                f"nodes={r['nodes']} edges={r['edges']}"
            )
        except Exception as exc:
            print(f"  {name}: FAIL {exc}")
    results.sort(key=lambda x: x["score"], reverse=True)
    print("\nRANKED:")
    for r in results:
        gap = target - r["score"]
        print(f"  {r['name']}: {r['score']:.4f} (gap {gap:+.4f})")
    if results:
        best = results[0]
        print(f"\nBEST: {best['name']} score={best['score']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())