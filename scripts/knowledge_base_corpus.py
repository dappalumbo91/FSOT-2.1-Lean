"""FSOT Knowledge Base unified transfer — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_unified_transfer(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_knowledge_base(data: dict) -> dict[str, Any]:
    counts = data.get("counts", {})
    return {
        "source_count": counts.get("sources"),
        "catalog_formulas": counts.get("catalog_formulas"),
        "resolved_formulas": counts.get("resolved_formulas"),
        "observable_citations": counts.get("observable_citations"),
    }