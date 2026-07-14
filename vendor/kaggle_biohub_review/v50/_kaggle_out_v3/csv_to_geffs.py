from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl
import tracksdata as td




def build_graph_from_rows(
    node_rows: pl.DataFrame,
    edge_rows: pl.DataFrame,
) -> td.graph.InMemoryGraph:
    """Rebuild a tracksdata graph from one dataset's node and edge rows.

    tracksdata assigns fresh node ids, so CSV ``node_id``s are remapped when
    adding edges (matching is spatial, not by id).
    """
    graph = td.graph.InMemoryGraph()
    for key in ("z", "y", "x"):
        graph.add_node_attr_key(key, pl.Float64, -999999.0)

    assigned = graph.bulk_add_nodes(
        node_rows.select(
            pl.col("t").cast(pl.Int64),
            pl.col("z").cast(pl.Float64),
            pl.col("y").cast(pl.Float64),
            pl.col("x").cast(pl.Float64),
        ).to_dicts()
    )
    id_map = dict(zip(node_rows["node_id"].to_list(), assigned, strict=True))

    if edge_rows.height:
        graph.bulk_add_edges(
            [
                {"source_id": id_map[s], "target_id": id_map[t]}
                for s, t in zip(
                    edge_rows["source_id"].to_list(), edge_rows["target_id"].to_list(), strict=True
                )
            ]
        )

    return graph


def csv_to_geffs(
    csv_path: Path | str,
    out_dir: Path | str,
    overwrite: bool = True,
) -> list[Path]:
    """Convert a submission CSV into one ``{dataset}.geff`` in ``out_dir``; return their paths."""
    csv_path = Path(csv_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pl.read_csv(
        csv_path,
        columns=["dataset", "row_type", "node_id", "t", "z", "y", "x", "source_id", "target_id"],
    )

    written: list[Path] = []
    for (name,), group in df.group_by("dataset"):
        node_rows = group.filter(pl.col("row_type") == "node")
        edge_rows = group.filter(pl.col("row_type") == "edge")

        graph = build_graph_from_rows(node_rows, edge_rows)
        out_path = out_dir / f"{name}.geff"
        if overwrite and out_path.exists():
            import shutil

            if out_path.is_dir():
                shutil.rmtree(out_path)
            else:
                out_path.unlink()
        graph.to_geff(out_path)
        written.append(out_path)
        print(f"{name}: {node_rows.height} nodes, {edge_rows.height} edges -> {out_path}")

    print(f"\nWrote {len(written)} geffs to {out_dir}")
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a submission CSV into one .geff per dataset.")
    parser.add_argument("--csv", type=Path, required=True, help="Submission CSV path.")
    parser.add_argument("--out-dir", type=Path, required=True, help="Output directory for .geff files.")
    parser.add_argument("--no-overwrite", action="store_true", help="Do not overwrite existing geffs.")
    args = parser.parse_args()

    csv_to_geffs(args.csv, args.out_dir, overwrite=not args.no_overwrite)


if __name__ == "__main__":
    main()