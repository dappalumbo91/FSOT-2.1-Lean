"""FSOT biological evolution sim — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_operons(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_best_organism(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_evolution(operons: dict, best: dict) -> dict[str, Any]:
    total_bp = sum(v.get("length", 0) for v in operons.values())
    return {
        "operon_count": len(operons),
        "total_bp": total_bp,
        "best_id": best.get("id"),
        "fitness": best.get("fitness"),
        "biological_capacity": best.get("biological_capacity"),
        "best_operon_count": len(best.get("operons", {})),
    }