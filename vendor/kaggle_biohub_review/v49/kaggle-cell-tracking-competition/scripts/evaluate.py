#!/usr/bin/env python
"""Score predicted ``.geff`` graphs against ground-truth ``.geff`` graphs.

Evaluates every dataset whose name appears in **both** ``--pred-dir`` and
``--gt-dir`` (others are skipped). No images are loaded: ground-truth tracks
come from the ``.geff`` and the voxel scale from the dataset's ``.zarr``
metadata (falling back to :data:`~tracking_cellmot.io.DEFAULT_SCALE`).

Reports the run-level score — sample-size-weighted adjusted edge Jaccard plus
``0.1 x`` division Jaccard — via :func:`tracking_cellmot.metrics.summarise`.

Usage:
    python scripts/evaluate.py --pred-dir out_geffs --gt-dir data/train
"""

from __future__ import annotations

import argparse
from pathlib import Path

import tracksdata as td
from geff import GeffMetadata

from tracking_cellmot.io import DEFAULT_SCALE, open_dataset
from tracking_cellmot.metrics import (
    evaluate as compute_metric,
    node_recall,
    per_sample_metrics,
    summarise,
)

from dataspec import DATASET_PATH


def _load_graph(geff_path: Path) -> td.graph.BaseGraph:
    result = td.graph.IndexedRXGraph.from_geff(geff_path)
    return result[0] if isinstance(result, tuple) else result


def _read_scale(gt_dir: Path, name: str) -> tuple[float, float, float]:
    """Return the dataset's (Z, Y, X) voxel scale, or DEFAULT_SCALE if no zarr.

    Only zarr metadata is read — the image itself is never loaded.
    """
    try:
        return open_dataset(gt_dir / name, load_image=False).scale
    except FileNotFoundError:
        return DEFAULT_SCALE


def _read_estimated_n_total(geff_path: Path) -> float:
    """Read ``estimated_number_of_nodes`` from a GEFF's metadata (NaN if absent)."""
    try:
        meta = GeffMetadata.read(geff_path)
    except Exception:
        return float("nan")
    val = (meta.extra or {}).get("estimated_number_of_nodes")
    return float(val) if val is not None else float("nan")


def evaluate_pairs(
    pred_dir: Path | str,
    gt_dir: Path | str,
    max_distance: float = 7.0,
) -> tuple[list[dict], list[str]]:
    """Score every dataset present in both dirs; return (per-sample rows, skipped).

    Rows are :func:`tracking_cellmot.metrics.per_sample_metrics` dicts, ready for
    :func:`tracking_cellmot.metrics.summarise`. No images are loaded.
    """
    pred_dir = Path(pred_dir)
    gt_dir = Path(gt_dir)

    pred_names = {p.stem for p in pred_dir.glob("*.geff")}
    gt_names = {p.stem for p in gt_dir.glob("*.geff")}
    names = sorted(pred_names & gt_names)
    print(f"{len(names)} datasets in both pred and GT (of {len(pred_names)} pred / {len(gt_names)} GT)")

    rows: list[dict] = []
    skipped: list[str] = []
    for name in names:
        gt_path = gt_dir / f"{name}.geff"
        try:
            pred_graph = _load_graph(pred_dir / f"{name}.geff")
            gt_graph = _load_graph(gt_path)
            scale = _read_scale(gt_dir, name)
            er = compute_metric(pred_graph, gt_graph, scale=scale, max_distance=max_distance)
            recall = (
                node_recall(pred_graph, gt_graph)
                if pred_graph.num_edges() > 0 and pred_graph.num_nodes() > 0
                else 0.0
            )
            n_total = _read_estimated_n_total(gt_path)
        except Exception as exc:  # unreadable/partial geff, etc.
            skipped.append(name)
            print(f"  SKIP {name}: {type(exc).__name__}: {exc}")
            continue

        rows.append(per_sample_metrics(er, n_total, recall))
        print(
            f"  {name}: edge TP/FP/FN={er.edge_tp}/{er.edge_fp}/{er.edge_fn} "
            f"div TP/FP/FN={er.division_tp}/{er.division_fp}/{er.division_fn} "
            f"n_pred={er.num_pred_nodes}"
        )

    if skipped:
        print(f"\nSkipped {len(skipped)} unreadable datasets: {skipped}")
    return rows, skipped


def evaluate_run(run: dict, max_distance: float = 7.0) -> list[dict]:
    """Score the predicted geffs in ``run['dir']`` against GT in ``DATASET_PATH``.

    Thin shim so ``scripts/predict_unet_transformer.py`` can evaluate a fresh
    prediction run right after inference.
    """
    rows, _ = evaluate_pairs(run["dir"], DATASET_PATH, max_distance=max_distance)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Score predicted .geff graphs against ground-truth .geff graphs.")
    parser.add_argument("--pred-dir", type=Path, required=True, help="Directory of predicted .geff files.")
    parser.add_argument("--gt-dir", type=Path, required=True, help="Directory of ground-truth .geff files.")
    parser.add_argument("--max-distance", type=float, default=7.0)
    args = parser.parse_args()

    rows, _ = evaluate_pairs(args.pred_dir, args.gt_dir, max_distance=args.max_distance)
    s = summarise(rows)
    print("\n=== Summary ===")
    print(
        f"n={s['n']}  score={s['score']:.4f}  "
        f"edge_jaccard={s['edge_jaccard']:.4f}  "
        f"adj_edge_jaccard={s['adj_edge_jaccard']:.4f} (n_adj={s['n_adj']})  "
        f"division_jaccard={s['division_jaccard']:.4f} "
        f"(TP={s['division_tp']} FP={s['division_fp']} FN={s['division_fn']})  "
        f"node_recall={s['node_recall']:.4f}"
    )


if __name__ == "__main__":
    main()
