#!/usr/bin/env python3
"""Pre-flight validation mirroring Kaggle's csv_to_geffs + competition rules."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parent
_REPO = ROOT / "kaggle-cell-tracking-competition"
for p in (
    Path("/kaggle/working/cellmot_bundle/scripts"),
    Path("/kaggle/working"),
    _REPO / "scripts",
    _REPO / "src",
    ROOT,
):
    if p.exists():
        sys.path.insert(0, str(p))

from csv_to_geffs import build_graph_from_rows, csv_to_geffs  # noqa: E402

COLUMNS = (
    "id", "dataset", "row_type", "node_id", "t", "z", "y", "x", "source_id", "target_id",
)
TEST_DATASETS = (
    "44b6_0113de3b",
    "44b6_0b24845f",
    "6bba_05b6850b",
    "6bba_05db0fb1",
)


def validate_csv(csv_path: Path, strict_datasets: bool = True) -> list[str]:
    errors: list[str] = []
    df = pl.read_csv(csv_path)

    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        errors.append(f"missing columns: {missing}")
        return errors

    if df["id"].null_count():
        errors.append("null values in id column")
    if df["id"].n_unique() != df.height:
        errors.append("id column must be unique")

    datasets = sorted(df["dataset"].unique().to_list())
    if strict_datasets and datasets != list(TEST_DATASETS):
        errors.append(f"expected datasets {TEST_DATASETS}, got {datasets}")

    for name in datasets:
        group = df.filter(pl.col("dataset") == name)
        nodes = group.filter(pl.col("row_type") == "node")
        edges = group.filter(pl.col("row_type") == "edge")

        if nodes.height == 0:
            errors.append(f"{name}: no node rows")
            continue
        if edges.height == 0:
            errors.append(f"{name}: no edge rows")

        node_ids = nodes["node_id"].to_list()
        if min(node_ids) != 1:
            errors.append(f"{name}: node_id must start at 1, got min={min(node_ids)}")
        if len(set(node_ids)) != len(node_ids):
            errors.append(f"{name}: duplicate node_id values in node rows")

        bad_nodes = nodes.filter(
            (pl.col("source_id") != -1) | (pl.col("target_id") != -1)
        )
        if bad_nodes.height:
            errors.append(f"{name}: {bad_nodes.height} node rows have non -1 source/target")

        bad_edges = edges.filter(
            (pl.col("node_id") != -1)
            | (pl.col("t") != -1)
            | (pl.col("z") != -1)
            | (pl.col("y") != -1)
            | (pl.col("x") != -1)
        )
        if bad_edges.height:
            errors.append(f"{name}: {bad_edges.height} edge rows have invalid placeholder fields")

        node_set = set(node_ids)
        for col in ("source_id", "target_id"):
            bad = edges.filter(~pl.col(col).is_in(list(node_set)))
            if bad.height:
                errors.append(f"{name}: {bad.height} edges reference missing {col}")

        dup_edges = edges.group_by(["source_id", "target_id"]).len().filter(pl.col("len") > 1)
        if dup_edges.height:
            errors.append(f"{name}: {dup_edges.height} duplicate (source_id, target_id) pairs")

        # Official loader must succeed (strict node_id zip).
        try:
            build_graph_from_rows(nodes, edges)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: csv_to_geffs build failed: {exc}")

        t_max = int(nodes["t"].max())
        t_min = int(nodes["t"].min())
        if t_min < 0:
            errors.append(f"{name}: node t < 0")
        if t_max < 99:
            errors.append(f"{name}: only covers t=0..{t_max}, expected 0..99")

    return errors


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate submission.csv before Kaggle upload")
    ap.add_argument("csv", type=Path)
    ap.add_argument("--score", action="store_true", help="Also score against train GT")
    ap.add_argument("--gt-dir", type=Path, default=Path(r"D:\Kaggle_Biohub_Data\train"))
    ap.add_argument("--no-strict-datasets", action="store_true")
    args = ap.parse_args()

    errors = validate_csv(args.csv, strict_datasets=not args.no_strict_datasets)
    if errors:
        print("INVALID submission:")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)

    print(f"VALID: {args.csv} ({pl.read_csv(args.csv).height} rows)")

    with tempfile.TemporaryDirectory(prefix="biohub_validate_") as tmp:
        csv_to_geffs(args.csv, Path(tmp))
        print(f"csv_to_geffs round-trip OK ({len(list(Path(tmp).glob('*.geff')))} geffs)")

    if args.score:
        from kaggle_submission_score import score_csv  # noqa: WPS433

        out = score_csv(args.csv, args.gt_dir)
        print(f"Train proxy score: {out['score']:.4f} (adj={out['adj_edge_jaccard']:.4f})")


if __name__ == "__main__":
    main()