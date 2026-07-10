#!/usr/bin/env python3
"""Build higgs_mass benchmark from FO-213 SMILES intrinsic formula."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "higgs_mass_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from higgs_mass_formula_eval import evaluate_higgs_mass  # noqa: E402


def build() -> dict:
    doc = evaluate_higgs_mass()
    records = [
        {
            "lab": "higgs_mass",
            "property": "m_H_GeV",
            "rule_id": doc["rule_id"],
            "computed": doc["computed_gev"],
            "measured": doc["measured_gev"],
            "error_pct": doc["error_pct"],
            "eval_kind": "live_formula",
            "formula": doc["formula"],
        },
        {
            "lab": "higgs_mass",
            "property": "m_H_MeV",
            "rule_id": doc["rule_id"],
            "computed": doc["computed_mev"],
            "measured": doc["measured_gev"] * 1000.0,
            "error_pct": doc["error_pct"],
            "eval_kind": "live_formula",
        },
    ]
    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": ["vendor/smiles/FSOT_SMILES_Lab_Dataset.json", "scripts/higgs_mass_formula_eval.py"],
        "maps_to_lean": ["particle"],
        "rule_id": doc["rule_id"],
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
    print(f"  m_H={doc['records'][0]['computed']:.6f} GeV  err={doc['records'][0]['error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())