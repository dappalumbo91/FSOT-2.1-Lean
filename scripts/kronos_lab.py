"""Kronos FSOT metrology — shared loaders."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def load_kronos_summary(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def summarize_kronos(rows: list[dict]) -> dict[str, Any]:
    errs = [float(r["kronos_fractional_error"]) for r in rows if r.get("kronos_fractional_error")]
    unc = [float(r["record_fractional_uncertainty"]) for r in rows if r.get("record_fractional_uncertainty")]
    return {
        "run_count": len(rows),
        "best_fractional_error": min(errs) if errs else None,
        "mean_fractional_error": sum(errs) / len(errs) if errs else None,
        "record_fractional_uncertainty": unc[0] if unc else None,
    }