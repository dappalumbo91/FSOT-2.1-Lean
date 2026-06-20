"""FSOT_Lean_Proofs formal constant bridge — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_formal_output(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_lean_proofs(data: dict) -> dict[str, Any]:
    constants = data.get("fsot_formalized_constants", [])
    proven = [c for c in constants if c.get("domain_proven")]
    return {
        "formal_constant_count": len(constants),
        "domain_proven_count": len(proven),
        "formal_names": [c["formal_name"] for c in constants],
    }