"""Parse FSOT BlackHole Thermo Thesis 2026 observable table."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


TABLE_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|"
)


def parse_thesis_table(md_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    in_table = False
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| # | Observable |"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table:
            if not line.startswith("|"):
                break
            m = TABLE_ROW_RE.match(line.strip())
            if not m:
                continue
            idx, name, formula, computed, target, err, tier = [g.strip() for g in m.groups()]
            try:
                error_pct = float(err.replace("%", ""))
            except ValueError:
                error_pct = None
            rows.append({
                "index": int(idx),
                "name": name,
                "formula": formula,
                "computed": computed,
                "target": target,
                "error_pct": error_pct,
                "tier": tier,
            })
    return rows


def summarize_blackhole(rows: list[dict]) -> dict[str, Any]:
    measured = [r for r in rows if r.get("error_pct") is not None]
    max_err = max((r["error_pct"] for r in measured), default=0.0)
    within_2 = sum(1 for r in measured if r["error_pct"] <= 2.0)
    return {
        "observable_count": len(rows),
        "measured_count": len(measured),
        "within_target_2pct": within_2,
        "max_error_pct": max_err,
        "strong_tier_count": sum(1 for r in rows if r.get("tier") == "STRONG"),
    }