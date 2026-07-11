"""Load and summarize FSOT strict-empirical formula corpus (per-formula observable checks)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_strict_empirical_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def observable_key(row: dict[str, Any]) -> tuple[str, str, str]:
    """Dedup key: same formula+target across projects counts once."""
    return (
        str(row.get("concept_name") or ""),
        str(row.get("formula_canonical") or row.get("formula_publication") or ""),
        str(row.get("target_quantity") or ""),
    )


def err_pct_from_values(target: float, computed: float) -> float:
    if target == 0.0:
        return abs(computed) * 100.0
    return abs(computed - target) / abs(target) * 100.0


def summarize_formula_corpus(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    matched = 0
    within_target = 0
    within_tolerable = 0
    max_error_pct = 0.0
    projects: dict[str, int] = {}
    unique_keys: set[tuple[str, str, str]] = set()
    unique_matched = 0
    unique_within_target = 0
    unique_within_tolerable = 0

    for row in rows:
        outcome = row.get("outcome") or {}
        if str(outcome.get("matched")).lower() == "true":
            matched += 1
        try:
            err = float(outcome.get("error_pct", 999))
        except (TypeError, ValueError):
            err = 999.0
        max_error_pct = max(max_error_pct, err)
        if err <= 2.0:
            within_target += 1
        if err <= 5.0:
            within_tolerable += 1
        proj = row.get("project") or "unknown"
        projects[proj] = projects.get(proj, 0) + 1

        key = observable_key(row)
        if key in unique_keys:
            continue
        unique_keys.add(key)
        if str(outcome.get("matched")).lower() == "true":
            unique_matched += 1
        if err <= 2.0:
            unique_within_target += 1
        if err <= 5.0:
            unique_within_tolerable += 1

    top_projects = sorted(projects.items(), key=lambda x: -x[1])[:10]
    unique_total = len(unique_keys)
    triplication = round(total / unique_total, 3) if unique_total else 1.0
    return {
        "records_total": total,
        "unique_observables": unique_total,
        "project_triplication_factor": triplication,
        "matched_count": matched,
        "unique_matched_count": unique_matched,
        "unmatched_count": total - matched,
        "within_target_2pct": within_target,
        "unique_within_target_2pct": unique_within_target,
        "within_tolerable_5pct": within_tolerable,
        "unique_within_tolerable_5pct": unique_within_tolerable,
        "max_error_pct": max_error_pct,
        "top_project_count": len(top_projects),
        "top_projects": [{"project": p, "records": c} for p, c in top_projects],
    }