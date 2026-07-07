#!/usr/bin/env python3
"""Materials engineering — mechanical/thermal SMILES observables."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "materials_engineering_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import smiles_dataset_path  # noqa: E402

ENGINEERING_SECTIONS = {
    "\u00a734 Young's Modulus",
    "\u00a737 Thermal \u03ba",
    "\u00a762 Bulk Modulus",
    "\u00a770 Shear Modulus",
    "\u00a773 Thermal Expansion",
    "\u00a784 Poisson Ratio \u03bd",
    "\u00a785 Thermal Diffusivity",
}


def build() -> dict:
    smiles = smiles_dataset_path()
    doc = json.loads(smiles.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        if section not in ENGINEERING_SECTIONS:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "materials_engineering_lab",
                "property": section,
                "name": row.get("name"),
                "computed": row.get("computed_value"),
                "measured": row.get("target_value"),
                "error_pct": float(err),
            }
        )
    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(smiles),
        "maps_to_lean": ["material", "energy"],
        "D_eff": 14,
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
    print(f"  records: {doc['record_count']}  median_err: {doc['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())