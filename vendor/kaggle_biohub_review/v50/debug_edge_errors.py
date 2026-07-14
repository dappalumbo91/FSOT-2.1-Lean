#!/usr/bin/env python3
"""Print FP/FN edges on train GT subgraph — targets the 48/3/2 ceiling."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
_REPO = ROOT / "kaggle-cell-tracking-competition"
for p in (_REPO / "src", _REPO / "scripts", ROOT):
    sys.path.insert(0, str(p))

import tracksdata as td
from tracking_cellmot.metrics import evaluate, _evaluate_matched_graph
from csv_to_geffs import csv_to_geffs
import tempfile

K = td.DEFAULT_ATTR_KEYS


def load_pred_graph(csv_path: Path) -> td.graph.BaseGraph:
    with tempfile.TemporaryDirectory() as tmp:
        csv_to_geffs(csv_path, Path(tmp))
        g = td.graph.IndexedRXGraph.from_geff(Path(tmp) / "44b6_0113de3b.geff")
        return g[0] if isinstance(g, tuple) else g


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=ROOT / "submission_v50.csv")
    args = ap.parse_args()
    csv_path = args.csv
    gt_path = Path(r"D:\Kaggle_Biohub_Data\train\44b6_0113de3b.geff")
    pred = load_pred_graph(csv_path)
    gt = td.graph.IndexedRXGraph.from_geff(gt_path)
    gt = gt[0] if isinstance(gt, tuple) else gt

    er = evaluate(pred, gt, max_distance=7.0)
    print(f"edge TP={er.edge_tp} FP={er.edge_fp} FN={er.edge_fn}")
    print(f"pred_nodes={er.num_pred_nodes} gt_nodes={gt.num_nodes()} gt_edges={gt.num_edges()}")

    edge_attrs = _evaluate_matched_graph(pred, gt)
    nodes = pred.node_attrs(attr_keys=[K.NODE_ID, K.T, "z", "y", "x", K.MATCHED_NODE_ID])

    fps = edge_attrs.filter(
        edge_attrs["pred_valid"] & ~edge_attrs[K.MATCHED_EDGE_MASK]
    )
    tps = edge_attrs.filter(edge_attrs[K.MATCHED_EDGE_MASK])

    print(f"\nFALSE POSITIVES ({fps.height}):")
    for row in fps.iter_rows(named=True):
        src, tgt = int(row[K.EDGE_SOURCE]), int(row[K.EDGE_TARGET])
        sn = nodes.filter(nodes[K.NODE_ID] == src)
        tn = nodes.filter(nodes[K.NODE_ID] == tgt)
        if sn.height and tn.height:
            s, t = sn.row(0, named=True), tn.row(0, named=True)
            print(
                f"  pred {src}->{tgt}  t={int(s[K.T])}->{int(t[K.T])} "
                f"({int(s['z'])},{int(s['y'])},{int(s['x'])})->({int(t['z'])},{int(t['y'])},{int(t['x'])})"
            )

    gt_edges = gt.edge_attrs(attr_keys=[K.EDGE_SOURCE, K.EDGE_TARGET])
    matched_gt = set(
        int(x)
        for x in nodes.filter(
            nodes[K.MATCHED_NODE_ID].is_not_null() & (nodes[K.MATCHED_NODE_ID] != -1)
        )[K.MATCHED_NODE_ID].to_list()
    )
    print(f"\nGT edges on matched nodes ({gt_edges.height}):")
    fn_edges: list[tuple[int, int]] = []
    for row in gt_edges.iter_rows(named=True):
        gs, gt_id = int(row[K.EDGE_SOURCE]), int(row[K.EDGE_TARGET])
        if gs not in matched_gt or gt_id not in matched_gt:
            continue
        pred_src = nodes.filter(nodes[K.MATCHED_NODE_ID] == gs)[K.NODE_ID]
        pred_tgt = nodes.filter(nodes[K.MATCHED_NODE_ID] == gt_id)[K.NODE_ID]
        if pred_src.len() == 0 or pred_tgt.len() == 0:
            continue
        ps, pt = int(pred_src[0]), int(pred_tgt[0])
        has = edge_attrs.filter(
            (edge_attrs[K.EDGE_SOURCE] == ps) & (edge_attrs[K.EDGE_TARGET] == pt)
            & edge_attrs[K.MATCHED_EDGE_MASK]
        ).height > 0
        if not has:
            fn_edges.append((gs, gt_id, ps, pt))
            gn = gt.node_attrs(attr_keys=[K.NODE_ID, K.T, "z", "y", "x"])
            s = gn.filter(gn[K.NODE_ID] == gs).row(0, named=True)
            t = gn.filter(gn[K.NODE_ID] == gt_id).row(0, named=True)
            print(
                f"  FN gt {gs}->{gt_id}  t={int(s[K.T])}->{int(t[K.T])} "
                f"pred_nodes {ps}->{pt}"
            )
    print(f"\nFALSE NEGATIVES: {len(fn_edges)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())