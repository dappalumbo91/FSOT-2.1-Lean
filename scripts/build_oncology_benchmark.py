#!/usr/bin/env python3
"""Oncology observables — SMILES drug/enzyme affinity + biology strict operon bridge."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMILES_JSON = Path(r"C:\Users\damia\Desktop\FSOT SMILES Lab\FSOT_SMILES_Lab_Dataset.json")
BIO_STRICT = ROOT / "data" / "biology_strict_empirical.json"
OUTPUT = ROOT / "data" / "oncology_benchmark.json"

ONCOLOGY_SECTIONS = {
    "\u00a723 Drug pKd",
    "\u00a765 Enzyme pKi",
    "\u00a724 Enzyme kcat",
    "\u00a735 Michaelis Km",
    "\u00a721 Protein \u0394G",
}


def _smiles_records() -> list[dict]:
    if not SMILES_JSON.exists():
        return []
    doc = json.loads(SMILES_JSON.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        if section not in ONCOLOGY_SECTIONS:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "oncology_lab",
                "property": section,
                "name": row.get("name"),
                "computed": row.get("computed_value"),
                "measured": row.get("target_value"),
                "error_pct": float(err),
                "source": "smiles_lab",
            }
        )
    return records


def _biology_strict_records() -> list[dict]:
    if not BIO_STRICT.exists():
        return []
    doc = json.loads(BIO_STRICT.read_text(encoding="utf-8"))
    records: list[dict] = []
    for row in doc.get("records") or []:
        if not row.get("strict"):
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "oncology_lab",
                "property": row.get("property"),
                "name": row.get("name"),
                "computed": row.get("computed"),
                "measured": row.get("measured"),
                "error_pct": float(err),
                "source": "biology_strict_lab",
            }
        )
    return records


def build() -> dict:
    records = _smiles_records() + _biology_strict_records()
    errs = [r["error_pct"] for r in records]
    smiles_n = sum(1 for r in records if r.get("source") == "smiles_lab")
    strict_n = sum(1 for r in records if r.get("source") == "biology_strict_lab")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [str(SMILES_JSON), str(BIO_STRICT)],
        "maps_to_lean": ["medical", "biological"],
        "D_eff": 14,
        "record_count": len(records),
        "observable_count": len(records),
        "smiles_record_count": smiles_n,
        "biology_strict_record_count": strict_n,
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
    print(f"  records: {doc['record_count']} (smiles={doc['smiles_record_count']} strict={doc['biology_strict_record_count']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())