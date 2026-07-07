"""iGEM Registry of Standard Biological Parts — shared loader."""

from __future__ import annotations

import json
from pathlib import Path


def load_registry(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_parts(catalog: dict) -> list[dict]:
    rows: list[dict] = []
    for part_id, body in (catalog.get("parts") or {}).items():
        if not isinstance(body, dict):
            continue
        rows.append(
            {
                "part_id": part_id,
                "type": body.get("type"),
                "length_bp": body.get("length_bp"),
                "gc_percent": body.get("gc_percent"),
                "description": body.get("description"),
                "status": body.get("status"),
            }
        )
    return rows