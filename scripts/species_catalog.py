"""FSOT Machine & Molecule species catalog — shared by ingest and verification."""

from __future__ import annotations

import json
from pathlib import Path

CATALOG_CATEGORIES = ("metals", "molecules", "polymers")


def load_catalog(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_catalog(catalog: dict) -> list[dict]:
    rows: list[dict] = []
    for category in CATALOG_CATEGORIES:
        for species_id, body in catalog.get(category, {}).items():
            if not isinstance(body, dict):
                continue
            for prop, metrics in body.items():
                if prop.startswith("_") or not isinstance(metrics, dict):
                    continue
                rows.append({
                    "category": category,
                    "species_id": species_id,
                    "property": prop,
                    "target": metrics.get("target"),
                    "computed": metrics.get("computed"),
                    "error_pct": metrics.get("error_pct"),
                    "formula": metrics.get("formula"),
                    "unit": metrics.get("unit"),
                })
    return rows


def summarize_species(catalog: dict, rows: list[dict]) -> dict:
    species_counts = {c: len(catalog.get(c, {})) for c in CATALOG_CATEGORIES}
    errors = [r["error_pct"] for r in rows if r.get("error_pct") is not None]
    return {
        "category_counts": species_counts,
        "species_count": sum(species_counts.values()),
        "property_count": len(rows),
        "max_error_pct": max(errors) if errors else 0.0,
        "mean_error_pct": sum(errors) / len(errors) if errors else 0.0,
    }