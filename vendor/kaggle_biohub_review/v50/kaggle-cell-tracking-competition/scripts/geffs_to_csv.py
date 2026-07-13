from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl
import tracksdata as td

# Column order of the submission CSV (the ``id`` index column is prepended last).
COLUMNS: tuple[str, ...] = (
    "dataset", "row_type", "node_id", "t", "z", "y", "x", "source_id", "target_id",
)


def _load_graph(geff_path: Path) -> td.graph.BaseGraph:
    result = td.graph.IndexedRXGraph.from_geff(geff_path)
    return result[0] if isinstance(result, tuple) else result


def graph_to_rows(graph: td.graph.BaseGraph, name: str) -> pl.DataFrame:
    """Flatten one graph into node rows then edge rows (submission schema).

    Coordinates are rounded to int (integer-valued in submission space, so this
    round-trips exactly with ``csv_to_geffs``); unused per-row-type fields are ``-1``.
    """
    nodes = graph.node_attrs().select(
        pl.lit(name).alias("dataset"),
        pl.lit("node").alias("row_type"),
        pl.col("node_id").cast(pl.Int64),
        pl.col("t").cast(pl.Int64),
        pl.col("z").cast(pl.Float64).round(0).cast(pl.Int64),
        pl.col("y").cast(pl.Float64).round(0).cast(pl.Int64),
        pl.col("x").cast(pl.Float64).round(0).cast(pl.Int64),
        pl.lit(-1, dtype=pl.Int64).alias("source_id"),
        pl.lit(-1, dtype=pl.Int64).alias("target_id"),
    )
    edges = graph.edge_attrs().select(
        pl.lit(name).alias("dataset"),
        pl.lit("edge").alias("row_type"),
        pl.lit(-1, dtype=pl.Int64).alias("node_id"),
        pl.lit(-1, dtype=pl.Int64).alias("t"),
        pl.lit(-1, dtype=pl.Int64).alias("z"),
        pl.lit(-1, dtype=pl.Int64).alias("y"),
        pl.lit(-1, dtype=pl.Int64).alias("x"),
        pl.col("source_id").cast(pl.Int64),
        pl.col("target_id").cast(pl.Int64),
    )
    return pl.concat([nodes, edges])


def geffs_to_csv(in_dir: Path | str, csv_path: Path | str) -> Path:
    """Flatten every ``.geff`` in ``in_dir`` into one submission CSV; return its path."""
    in_dir = Path(in_dir)
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    geffs = sorted(in_dir.glob("*.geff"))
    frames: list[pl.DataFrame] = []
    for geff in geffs:
        graph = _load_graph(geff)
        frames.append(graph_to_rows(graph, geff.stem))
        print(f"{geff.stem}: {graph.num_nodes()} nodes, {graph.num_edges()} edges")

    if frames:
        table = pl.concat(frames)
    else:
        table = pl.DataFrame(schema={c: (pl.String if c in ("dataset", "row_type") else pl.Int64) for c in COLUMNS})
    table = table.with_row_index("id")

    table.write_csv(csv_path)
    print(f"\nWrote {table.height} rows from {len(geffs)} geffs to {csv_path}")
    return csv_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Flatten .geff graphs into a submission CSV.")
    parser.add_argument("--in-dir", type=Path, required=True, help="Directory of .geff files.")
    parser.add_argument("--csv", type=Path, required=True, help="Output submission CSV path.")
    args = parser.parse_args()

    geffs_to_csv(args.in_dir, args.csv)


if __name__ == "__main__":
    main()
