"""FSOT ΛCDM Wave-4 observable extraction — PMNS, CKM, Feigenbaum, nuclear, dark energy."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cosmology_lambda import load_fsot_compute, summarize_lambda


def wave4_observables(mod) -> list[dict[str, Any]]:
    """Wave-4 (16) PMNS/CKM/Feigenbaum/nuclear/dark-energy scales."""
    rows: list[dict[str, Any]] = []
    for r in mod.wave4():
        measured = float(r.measured) if r.measured is not None else None
        computed = float(r.computed)
        error_pct = None
        if measured is not None and measured != 0:
            error_pct = abs(computed - measured) / abs(measured) * 100.0
        rows.append({
            "wave": "wave4",
            "name": r.name,
            "formula": r.formula_str,
            "computed": computed,
            "measured": measured,
            "error_pct": error_pct,
        })
    return rows


def summarize_wave4(rows: list[dict]) -> dict[str, Any]:
    base = summarize_lambda(rows)
    return {
        "observable_count": base["observable_count"],
        "wave4_count": base["observable_count"],
        "measured_count": base["measured_count"],
        "max_error_pct": base["max_error_pct"],
        "mean_error_pct": base["mean_error_pct"],
    }