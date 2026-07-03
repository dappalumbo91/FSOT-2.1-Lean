#!/usr/bin/env python3
"""Pharmacology benchmark — ChEMBL molecular weight vs FSOT formula mass."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "pharmacology_chembl_cache.json"
OUTPUT = ROOT / "data" / "pharmacology_benchmark.json"

ATOMIC_MASS = {
    "H": 1.008,
    "He": 4.003,
    "Li": 6.94,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Na": 22.99,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "K": 39.098,
    "Ca": 40.078,
    "Fe": 55.845,
    "Br": 79.904,
    "I": 126.904,
}


def formula_mass(formula: str) -> float | None:
    if not formula:
        return None
    total = 0.0
    for elem, count in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if elem not in ATOMIC_MASS:
            return None
        n = int(count) if count else 1
        total += ATOMIC_MASS[elem] * n
    return total if total > 0 else None


def build(cache_path: Path = CACHE) -> dict:
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_pharmacology_chembl.py first: {cache_path}")
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, authority_path = load_fsot_compute()
    S_med = float(mod.domain_scalar("Biochemistry"))

    records: list[dict] = []
    for row in doc.get("molecules") or []:
        props = row.get("molecule_properties") or {}
        measured = props.get("full_mwt")
        formula = props.get("molecular_formula") or props.get("full_molformula")
        if measured is None or not formula:
            continue
        computed = formula_mass(str(formula))
        if computed is None:
            continue
        # Medical-scalar calibration gate (±0.5% base + |S| drift)
        tol_pct = 0.5 + abs(S_med) * 0.2
        err = abs(computed - float(measured)) / float(measured) * 100.0
        records.append(
            {
                "lab": "pharmacology_lab",
                "property": "molecular_weight",
                "name": row.get("pref_name") or row.get("molecule_chembl_id"),
                "chembl_id": row.get("molecule_chembl_id"),
                "formula": formula,
                "computed": round(computed, 4),
                "measured": float(measured),
                "error_pct": err,
                "within_band": err <= tol_pct,
                "S_medical": round(S_med, 6),
            }
        )

    errs = [r["error_pct"] for r in records]
    within = sum(1 for r in records if r.get("within_band"))
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "ChEMBL_max_phase_4",
        "record_count": len(records),
        "observable_count": len(records),
        "within_band_count": within,
        "within_band_rate": within / len(records) if records else 0.0,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "maps_to_lean": ["medical", "chemical"],
        "D_eff": 14,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=CACHE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        bench = build(args.cache)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {bench['record_count']}  median_err: {bench.get('median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())