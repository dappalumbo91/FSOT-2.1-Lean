"""FSOT ΛCDM observable extraction — shared by ingest and verification."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


def load_fsot_compute(path: Path):
    spec = importlib.util.spec_from_file_location("fsot_compute_cosmology", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def lambda_cdm_observables(mod) -> list[dict[str, Any]]:
    """Wave-1 (5) + Wave-2 (10) + Wave-3 (15) = 30 observables."""
    w1 = mod.wave1()
    w2 = mod.wave2()[:10]
    w3 = mod.wave3()
    rows: list[dict[str, Any]] = []
    for wave_group, results in (
        ("wave1", w1),
        ("wave2", w2),
        ("wave3", w3),
    ):
        for r in results:
            measured = float(r.measured) if r.measured is not None else None
            computed = float(r.computed)
            error_pct = None
            if measured is not None and measured != 0:
                error_pct = abs(computed - measured) / abs(measured) * 100.0
            rows.append({
                "wave": wave_group,
                "name": r.name,
                "formula": r.formula_str,
                "computed": computed,
                "measured": measured,
                "error_pct": error_pct,
            })
    return rows


def summarize_lambda(rows: list[dict]) -> dict:
    with_measured = [r for r in rows if r.get("measured") is not None]
    errors = [r["error_pct"] for r in with_measured if r.get("error_pct") is not None]
    return {
        "observable_count": len(rows),
        "wave1_count": sum(1 for r in rows if r["wave"] == "wave1"),
        "wave2_count": sum(1 for r in rows if r["wave"] == "wave2"),
        "wave3_count": sum(1 for r in rows if r["wave"] == "wave3"),
        "measured_count": len(with_measured),
        "max_error_pct": max(errors) if errors else 0.0,
        "mean_error_pct": sum(errors) / len(errors) if errors else 0.0,
    }