"""Load certified SMILES formula improvements from desktop lab."""

from __future__ import annotations

import re
from pathlib import Path

KNOWN_IMPROVEMENTS_PATH = (
    Path.home() / "Desktop" / "FSOT SMILES Lab" / "_temp_known_improvements.py"
)


def _section_num(section: str) -> str:
    m = re.match(r"(§\d+\w*)", section)
    return m.group(1) if m else section[:12]


def load_known_improvements() -> dict[tuple[str, str], tuple[str, float, float]]:
    if not KNOWN_IMPROVEMENTS_PATH.exists():
        return {}
    ns: dict = {}
    exec(KNOWN_IMPROVEMENTS_PATH.read_text(encoding="utf-8"), ns)
    return ns.get("KNOWN_IMPROVEMENTS") or {}


def build_dataset_overrides(
    records: list[dict],
    *,
    min_error_pct: float | None = None,
) -> dict[tuple[str, str], dict[str, object]]:
    """Map known improvements onto dataset (section, name) keys."""
    known = load_known_improvements()
    if not known:
        return {}

    section_by_pair: dict[tuple[str, str], str] = {}
    error_by_pair: dict[tuple[str, str], float] = {}
    for row in records:
        sec = str(row.get("section") or "")
        name = str(row.get("name") or "")
        section_by_pair[(_section_num(sec), name)] = sec
        err = row.get("error_pct")
        if err is not None:
            error_by_pair[(_section_num(sec), name)] = float(err)

    overrides: dict[tuple[str, str], dict[str, object]] = {}
    for (ki_sec, name), (formula, value, err) in known.items():
        if min_error_pct is not None:
            current = error_by_pair.get((_section_num(ki_sec), name))
            if current is None or current <= min_error_pct:
                continue
        full_sec = section_by_pair.get((_section_num(ki_sec), name))
        if not full_sec:
            continue
        overrides[(full_sec, name)] = {
            "fsot_formula": formula,
            "computed_value": float(value),
            "error_pct": float(err),
            "unified_section": _section_num(full_sec),
        }
    return overrides