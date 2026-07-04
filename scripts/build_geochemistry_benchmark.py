#!/usr/bin/env python3
"""Geochemistry observables — SMILES mineral/geo sections + planetary bulk density overlap."""

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
PLANETARY_BENCH = ROOT / "data" / "planetary_structure_benchmark.json"
OUTPUT = ROOT / "data" / "geochemistry_benchmark.json"

GEOCHEMISTRY_SECTIONS = {
    "\u00a740 Ionic Radii",
    "\u00a741 Covalent Radii",
    "\u00a763 Lattice Param",
    "\u00a742 Binding E/A",
    "\u00a7101 Atomization \u0394H_at",
    "\u00a725 vdW Radii",
    "\u00a726 Polarizability",
    "\u00a758 log\u03b2 Stability",
}


def _smiles_records() -> list[dict]:
    if not SMILES_JSON.exists():
        return []
    doc = json.loads(SMILES_JSON.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        if section not in GEOCHEMISTRY_SECTIONS:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "geochemistry_lab",
                "property": section,
                "name": row.get("name"),
                "computed": row.get("computed_value"),
                "measured": row.get("target_value"),
                "error_pct": float(err),
                "source": "smiles_lab",
            }
        )
    return records


def _planetary_records() -> list[dict]:
    if not PLANETARY_BENCH.exists():
        return []
    doc = json.loads(PLANETARY_BENCH.read_text(encoding="utf-8"))
    records: list[dict] = []
    for row in doc.get("records") or []:
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "geochemistry_lab",
                "property": "planetary_bulk_density",
                "name": row.get("name"),
                "computed": row.get("computed"),
                "measured": row.get("measured"),
                "error_pct": float(err),
                "source": "planetary_structure_lab",
            }
        )
    return records


def build() -> dict:
    records = _smiles_records() + _planetary_records()
    errs = [r["error_pct"] for r in records]
    smiles_n = sum(1 for r in records if r.get("source") == "smiles_lab")
    planetary_n = sum(1 for r in records if r.get("source") == "planetary_structure_lab")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [str(SMILES_JSON), str(PLANETARY_BENCH)],
        "maps_to_lean": ["chemical", "galactic"],
        "D_eff": 15,
        "record_count": len(records),
        "observable_count": len(records),
        "smiles_record_count": smiles_n,
        "planetary_record_count": planetary_n,
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
    print(f"  records: {doc['record_count']} (smiles={doc['smiles_record_count']} planetary={doc['planetary_record_count']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())