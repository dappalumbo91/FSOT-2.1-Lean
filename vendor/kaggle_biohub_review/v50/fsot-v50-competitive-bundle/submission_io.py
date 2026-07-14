#!/usr/bin/env python3
"""Torch-free submission CSV writer for CPU-only Kaggle runs."""

from __future__ import annotations

from pathlib import Path


def write_submission_csv(rows: list[dict], out_path: str | Path) -> Path:
    import polars as pl

    out = Path(out_path)
    cols = [
        "dataset", "row_type", "node_id", "t", "z", "y", "x", "source_id", "target_id",
    ]
    table = pl.DataFrame(rows).select(cols).with_row_index("id")
    table = table.select(
        "id", "dataset", "row_type", "node_id", "t", "z", "y", "x", "source_id", "target_id",
    )
    table.write_csv(out)
    return out