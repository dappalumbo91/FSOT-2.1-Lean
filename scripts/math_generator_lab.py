"""Math generator FSOT formula comparisons — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_comparison_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_math_generator(data: dict) -> dict[str, Any]:
    comparisons = data.get("comparisons", [])
    errors = [
        float(c["relative_error_percent"])
        for c in comparisons
        if c.get("relative_error_percent") is not None
    ]
    constants = data.get("constants", {})
    return {
        "comparison_count": len(comparisons),
        "quantitative_count": len(errors),
        "max_error_pct": max(errors) if errors else 0.0,
        "mean_error_pct": sum(errors) / len(errors) if errors else 0.0,
        "c_eff": constants.get("c_eff"),
        "p_base": constants.get("p_base"),
    }