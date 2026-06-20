"""FSOT linguistics empirical anchors — shared loaders."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Any


def load_targets_csv(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rows.append({
                "name": row["name"],
                "measured": float(row["measured"]),
                "sigma": float(row["sigma"]),
                "unit": row.get("unit"),
                "group": row.get("group"),
                "source": row.get("source"),
            })
    return rows


def load_derivations_db(db_path: Path) -> dict[str, dict[str, Any]]:
    if not db_path.exists():
        return {}
    con = sqlite3.connect(db_path)
    try:
        query = """
        SELECT t.name, d.value, d.error_pct, d.description, d.status
        FROM linguistic_targets t
        JOIN derivations d ON d.target_id = t.target_id
        WHERE d.status IN ('hand', 'search-tight', 'search-loose')
          AND d.rowid IN (
            SELECT MIN(rowid) FROM derivations
            WHERE target_id = t.target_id
              AND status IN ('hand', 'search-tight', 'search-loose')
            GROUP BY target_id
          )
        """
        out: dict[str, dict[str, Any]] = {}
        for name, value, err, desc, status in con.execute(query):
            out[name] = {
                "computed": float(value),
                "error_pct": float(err) if err is not None else None,
                "formula": desc,
                "status": status,
            }
        return out
    finally:
        con.close()


def merge_targets(targets: list[dict], derivations: dict[str, dict]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for t in targets:
        d = derivations.get(t["name"], {})
        err = d.get("error_pct")
        if err is None and d.get("computed") is not None and t["measured"]:
            err = abs(d["computed"] - t["measured"]) / abs(t["measured"]) * 100.0
        rows.append({**t, **d, "error_pct": err})
    return rows


def summarize_linguistics(rows: list[dict]) -> dict[str, Any]:
    errors = [abs(r["error_pct"]) for r in rows if r.get("error_pct") is not None]
    return {
        "target_count": len(rows),
        "derived_count": sum(1 for r in rows if r.get("computed") is not None),
        "max_error_pct": max(errors) if errors else 0.0,
        "mean_error_pct": sum(errors) / len(errors) if errors else 0.0,
    }