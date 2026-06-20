"""FSOT magnetic string lattice — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_magnetic_strings(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_magnetic_strings(data: dict) -> dict[str, Any]:
    meta = data.get("metadata", {})
    strings = data.get("strings", [])
    aligned = sum(1 for s in strings if s.get("is_top_aligned"))
    return {
        "string_count": len(strings),
        "S_em": meta.get("S_em"),
        "S_ac": meta.get("S_ac"),
        "coherence_efficiency": meta.get("coherence_efficiency"),
        "top_aligned_count": aligned,
        "top_aligned_fraction": aligned / len(strings) if strings else 0.0,
        "final_mean_stability": meta.get("final_mean_stability"),
    }