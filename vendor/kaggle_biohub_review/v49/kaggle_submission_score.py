#!/usr/bin/env python3
"""Score a submission CSV against train ground-truth .geff files (competition proxy)."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_REPO = ROOT / "kaggle-cell-tracking-competition"
for p in (ROOT, _REPO / "src", _REPO / "scripts"):
    if p.exists():
        sys.path.insert(0, str(p))

from csv_to_geffs import csv_to_geffs  # noqa: E402


def score_csv(csv_path: Path | str, gt_dir: Path | str) -> dict[str, float]:
    import importlib.util

    eval_path = _REPO / "scripts" / "evaluate.py"
    spec = importlib.util.spec_from_file_location("biohub_evaluate", eval_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {eval_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    evaluate_pairs = mod.evaluate_pairs
    from tracking_cellmot.metrics import summarise  # noqa: E402

    csv_path = Path(csv_path)
    gt_dir = Path(gt_dir)
    with tempfile.TemporaryDirectory(prefix="biohub_score_") as tmp:
        pred_dir = Path(tmp) / "pred"
        csv_to_geffs(csv_path, pred_dir)
        rows, skipped = evaluate_pairs(pred_dir, gt_dir)
        if not rows:
            return {
                "score": 0.0,
                "adj_edge_jaccard": 0.0,
                "division_jaccard": 0.0,
                "datasets_scored": 0,
                "skipped": skipped,
            }
        summary = summarise(rows)
        return {
            "score": float(summary["score"]),
            "adj_edge_jaccard": float(summary["adj_edge_jaccard"]),
            "division_jaccard": float(summary["division_jaccard"]),
            "datasets_scored": len(rows),
            "skipped": skipped,
        }


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("csv", type=Path)
    ap.add_argument("--gt-dir", type=Path, default=Path(r"D:\Kaggle_Biohub_Data\train"))
    args = ap.parse_args()
    out = score_csv(args.csv, args.gt_dir)
    print(out)