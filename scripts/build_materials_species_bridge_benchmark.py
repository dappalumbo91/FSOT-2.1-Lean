#!/usr/bin/env python3
"""Materials engineering ↔ species-catalog machine bridge for overlapping metals."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "materials_species_bridge_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import rel_repo_path, smiles_dataset_path, species_catalog_path  # noqa: E402
from species_catalog import load_catalog  # noqa: E402

PROPERTY_MAP = {
    "\u00a737 Thermal \u03ba": "thermal_cond_W_mK",
    "\u00a762 Bulk Modulus": "bulk_GPa",
    "\u00a770 Shear Modulus": "shear_GPa",
    "\u00a773 Thermal Expansion": "expansion_e6_per_K",
    "\u00a784 Poisson Ratio \u03bd": "poisson_ratio",
}


def _metal_id(name: str) -> str | None:
    token = (name or "").split()[0]
    if len(token) <= 3 and token[0].isupper():
        return token
    return None


def build() -> dict:
    smiles_path = smiles_dataset_path()
    species_path = species_catalog_path()
    smiles_doc = json.loads(smiles_path.read_text(encoding="utf-8"))
    rows = smiles_doc.get("records") if isinstance(smiles_doc, dict) else smiles_doc
    catalog = load_catalog(species_path)
    metals = catalog.get("metals") or {}

    records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        prop_key = PROPERTY_MAP.get(section)
        if not prop_key:
            continue
        metal = _metal_id(row.get("name") or "")
        if not metal or metal not in metals:
            continue
        species_prop = metals[metal].get(prop_key)
        if not isinstance(species_prop, dict):
            continue
        smiles_val = row.get("computed_value")
        species_val = species_prop.get("computed")
        if smiles_val is None or species_val is None:
            continue
        smiles_val = float(smiles_val)
        species_val = float(species_val)
        denom = max(abs(species_val), 1e-12)
        err = abs(smiles_val - species_val) / denom * 100.0
        records.append(
            {
                "lab": "materials_species_bridge",
                "metal": metal,
                "property": section,
                "species_property": prop_key,
                "computed": smiles_val,
                "measured": species_val,
                "error_pct": err,
            }
        )

    errs = sorted(r["error_pct"] for r in records)
    overlap_metals = sorted({r["metal"] for r in records})
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(smiles_path), rel_repo_path(species_path)],
        "maps_to_lean": ["material", "energy"],
        "D_eff": 14,
        "overlap_metal_count": len(overlap_metals),
        "overlap_metals": overlap_metals,
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  records: {doc['record_count']}  metals: {doc['overlap_metal_count']}  "
        f"median_err: {doc['median_error_pct']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())