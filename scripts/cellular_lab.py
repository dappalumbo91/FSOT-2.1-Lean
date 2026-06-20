"""Soul Simulator + evolution sim cellular-domain loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evolution_lab import load_operons, summarize_evolution


def load_soul_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_cellular(soul: dict, operons_path: Path, best_path: Path | None = None) -> dict[str, Any]:
    evo = summarize_evolution(load_operons(operons_path), {})
    return {
        "soul_records_processed": soul.get("records_processed", 0),
        "soul_file_count": soul.get("file_count", 0),
        "soul_types": soul.get("types", {}),
        "evolution_operon_count": evo["operon_count"],
        "evolution_total_bp": evo["total_bp"],
        "domain": "cellular",
        "D_eff": 12,
    }