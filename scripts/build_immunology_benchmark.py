#!/usr/bin/env python3
"""Immunology / biochemistry observables from SMILES medical sections."""

from __future__ import annotations

import sys
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import smiles_dataset_path  # noqa: E402

SMILES_JSON = smiles_dataset_path()
OUTPUT = ROOT / "data" / "immunology_benchmark.json"

IMMUNOLOGY_SECTIONS = {
    "\u00a721 Protein \u0394G",
    "\u00a722 Amino Acid pKa",
    "\u00a723 Drug pKd",
    "\u00a724 Enzyme kcat",
    "\u00a735 Michaelis Km",
    "\u00a765 Enzyme pKi",
    "\u00a771 DNA Stacking \u0394G",
}


def build() -> dict:
    if not SMILES_JSON.exists():
        return {"record_count": 0, "records": [], "error": "SMILES dataset missing"}
    doc = json.loads(SMILES_JSON.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        if section not in IMMUNOLOGY_SECTIONS:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "immunology_lab",
                "property": section,
                "name": row.get("name"),
                "computed": float(row.get("computed_value") or row.get("computed") or 0),
                "measured": float(row.get("target_value") or row.get("measured") or 0),
                "error_pct": float(err),
                "fsot_formula": row.get("fsot_formula"),
            }
        )
    errs = [r["error_pct"] for r in records]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(SMILES_JSON),
        "maps_to_lean": ["medical", "biological"],
        "D_eff": 13,
        "record_count": len(records),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())