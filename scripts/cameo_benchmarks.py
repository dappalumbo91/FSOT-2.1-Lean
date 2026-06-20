"""Genetics CAMEO folding benchmarks — shared by ingest and verification."""

from __future__ import annotations

import csv
from pathlib import Path


def load_cameo_results(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rows.append({
                "pdb": row["pdb"],
                "pearson": float(row["pearson"]),
                "spearman": float(row["spearman"]),
                "top_l_prec": float(row["top_l_prec"]),
                "long_range_prec": float(row["long_range_prec"]),
            })
    return rows


def summarize_cameo(rows: list[dict], symbolic: dict | None = None) -> dict:
    def mean(col: str) -> float:
        vals = [r[col] for r in rows]
        return sum(vals) / len(vals) if vals else 0.0

    summary = {
        "benchmark_count": len(rows),
        "mean_pearson": mean("pearson"),
        "mean_spearman": mean("spearman"),
        "mean_top_l_prec": mean("top_l_prec"),
        "mean_long_range_prec": mean("long_range_prec"),
        "min_top_l_prec": min(r["top_l_prec"] for r in rows) if rows else 0.0,
    }
    if symbolic:
        summary.update(symbolic)
    return summary