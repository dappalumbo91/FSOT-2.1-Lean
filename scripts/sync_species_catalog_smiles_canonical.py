#!/usr/bin/env python3
"""Align species catalog computed values with SMILES Lab canonical formulas."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _phi_panel_offenders_audit import (  # noqa: E402
    SMILES_PATH,
    find_smiles_row,
    _smiles_lookup,
)
from tier_l_orbital_gap_fill_lib import (  # noqa: E402
    SPECIES_PATH,
    _iter_species_entries,
    _load_json,
)


def sync_catalog(*, min_error_pct: float = 0.5, phi_only: bool = False, dry_run: bool = False) -> dict:
    from tier_l_orbital_gap_fill_lib import _phi_in_formula  # noqa: E402

    smiles_doc = _load_json(SMILES_PATH)
    exact, fuzzy = _smiles_lookup(smiles_doc)
    catalog = _load_json(SPECIES_PATH)

    updated = 0
    skipped = 0
    changes: list[dict] = []

    for section, species, payload in _iter_species_entries(catalog):
        prop = str(payload.get("property") or "")
        formula = str(payload.get("formula") or "")
        err = float(payload.get("error_pct") or 0)
        if err < min_error_pct:
            continue
        if phi_only and not _phi_in_formula(formula):
            continue
        smiles_row = find_smiles_row(exact, fuzzy, species, prop, section)
        if not smiles_row:
            skipped += 1
            continue
        sf = smiles_row.get("fsot_formula")
        sc = smiles_row.get("computed_value")
        se = smiles_row.get("error_pct")
        if sf is None or sc is None or se is None:
            skipped += 1
            continue
        if sf == formula and abs(float(sc) - float(payload.get("computed") or 0)) < 1e-9:
            continue

        bucket = catalog
        for part in section.split("."):
            bucket = bucket[part]
        entry = bucket[species][prop]
        old = {
            "formula": entry.get("formula"),
            "computed": entry.get("computed"),
            "error_pct": entry.get("error_pct"),
        }
        entry["formula"] = sf
        entry["computed"] = float(sc)
        entry["error_pct"] = float(se)
        updated += 1
        changes.append(
            {
                "species": species,
                "property": prop,
                "old_error_pct": old["error_pct"],
                "new_error_pct": float(se),
                "old_formula": old["formula"],
                "new_formula": sf,
            }
        )

    if updated and not dry_run:
        SPECIES_PATH.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

    return {"updated": updated, "skipped": skipped, "changes": changes, "dry_run": dry_run}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-error", type=float, default=0.5, help="Only sync entries above this error %%")
    ap.add_argument("--phi-only", action="store_true", help="Only sync phi-formula morphogenetic panel entries")
    ap.add_argument("--all", action="store_true", help="Sync all SMILES-mapped properties regardless of error")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    min_err = 0.0 if args.all else args.min_error
    result = sync_catalog(min_error_pct=min_err, phi_only=args.phi_only, dry_run=args.dry_run)
    print(
        f"{'[dry-run] ' if result['dry_run'] else ''}"
        f"updated={result['updated']} skipped={result['skipped']}"
    )
    for row in sorted(result["changes"], key=lambda x: -float(x["old_error_pct"] or 0))[:40]:
        print(
            f"  {row['species']:<18} {row['property']:<22} "
            f"{float(row['old_error_pct']):6.3f}% -> {float(row['new_error_pct']):6.3f}%  "
            f"{row['old_formula']} -> {row['new_formula']}"
        )
    if len(result["changes"]) > 40:
        print(f"  ... and {len(result['changes']) - 40} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())