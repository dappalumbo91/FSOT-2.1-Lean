"""FSOT Fuel Lab compound profiles — shared by ingest and verification."""

from __future__ import annotations

import json
from pathlib import Path

FUEL_BATCH_GLOBS = (
    "fuel_profile_compound_lookup_batch.json",
    "fuel_profile_compound_lookup_batch2.json",
    "fuel_profile_compound_lookup_batch3.json",
    "fuel_profile_compound_lookup_batch4.json",
    "fuel_profile_compound_lookup_batch5.json",
    "fuel_profile_compound_lookup_batch6.json",
    "algae_fuel_lookup.json",
)


def load_profiles(fuel_root: Path) -> list[dict]:
    by_id: dict[str, dict] = {}
    for name in FUEL_BATCH_GLOBS:
        path = fuel_root / name
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for profile_id, body in data.items():
            if not isinstance(body, dict):
                continue
            entries = body.get("lookup_entries", {})
            rows = []
            comp_fraction = 0.0
            for key, entry in entries.items():
                etype = entry.get("type", "")
                result = entry.get("result")
                row = {
                    "key": key,
                    "type": etype,
                    "fraction": entry.get("fraction"),
                    "mass_kg": entry.get("mass_kg"),
                    "unit_cost": entry.get("unit_cost"),
                    "resolved": result is not None,
                    "molecular_formula": (result or {}).get("molecular_formula"),
                    "inchi_key": (result or {}).get("inchi_key"),
                    "name": (result or {}).get("name"),
                }
                rows.append(row)
                if etype == "composition" and entry.get("fraction") is not None:
                    comp_fraction += float(entry["fraction"])
            by_id[profile_id] = {
                "profile_id": profile_id,
                "profile_name": body.get("fuel_profile_name", profile_id),
                "source_file": name,
                "entry_count": len(rows),
                "resolved_count": sum(1 for r in rows if r["resolved"]),
                "composition_fraction_sum": comp_fraction,
                "rows": rows,
            }
    return list(by_id.values())


def summarize_fuel(profiles: list[dict]) -> dict:
    return {
        "profile_count": len(profiles),
        "entry_count": sum(p["entry_count"] for p in profiles),
        "resolved_count": sum(p["resolved_count"] for p in profiles),
        "source_files": len({p["source_file"] for p in profiles}),
    }