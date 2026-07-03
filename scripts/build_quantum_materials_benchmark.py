#!/usr/bin/env python3
"""Quantum materials — condensed-matter SMILES observables."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMILES_JSON = Path(r"C:\Users\damia\Desktop\FSOT SMILES Lab\FSOT_SMILES_Lab_Dataset.json")
OUTPUT = ROOT / "data" / "quantum_materials_benchmark.json"

QUANTUM_MATERIALS_SECTIONS = {
    "\u00a729 Dielectric \u03b5r",
    "\u00a733 Debye Temps",
    "\u00a738 Resistivity \u03c1",
    "\u00a752 \u00b9\u00b3C NMR \u03b4",
    "\u00a763 Lattice Param",
    "\u00a713 \u03c7m Magnetic",
    "\u00a719 NMR \u03b4",
    "\u00a731 Band Gaps",
    "\u00a755 \u03bceff Magnetic",
    "\u00a775 Superconducting Tc",
    "\u00a776 Magnetic Ordering T",
    "\u00a74b Lattice Energies",
    "\u00a718 Crystal Field \u0394o",
}


def build() -> dict:
    if not SMILES_JSON.exists():
        return {"record_count": 0, "records": [], "error": "SMILES dataset missing"}
    doc = json.loads(SMILES_JSON.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        if section not in QUANTUM_MATERIALS_SECTIONS:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "quantum_materials_lab",
                "property": section,
                "name": row.get("name"),
                "computed": row.get("computed_value"),
                "measured": row.get("target_value"),
                "error_pct": float(err),
            }
        )
    errs = [r["error_pct"] for r in records]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(SMILES_JSON),
        "maps_to_lean": ["material", "quantum"],
        "D_eff": 16,
        "record_count": len(records),
        "observable_count": len(records),
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