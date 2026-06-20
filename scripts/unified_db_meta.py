"""FSOT Unified Database verification meta-certificate — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_verification_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_unified_db(report: dict) -> dict[str, Any]:
    counts = report.get("candidate_counts", {})
    numeric = report.get("numeric_evaluation", {})
    checkpoint = report.get("checkpoint", {}).get("stats", {})
    return {
        "total_candidates": counts.get("total"),
        "foundation_candidates": counts.get("foundation"),
        "current_candidates": counts.get("current"),
        "strict_empirical": counts.get("strict_empirical"),
        "with_error_pct": counts.get("with_error_pct"),
        "evaluation_ok": numeric.get("evaluation_ok"),
        "evaluation_failed": numeric.get("evaluation_failed"),
        "processed_total": checkpoint.get("processed_total"),
        "done_total": checkpoint.get("done_total"),
        "evaluator_version": numeric.get("evaluator_version"),
    }