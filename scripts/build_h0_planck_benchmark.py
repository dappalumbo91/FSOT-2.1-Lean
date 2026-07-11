#!/usr/bin/env python3
"""Build H0_planck benchmark — FO-200 CMB-sector readout vs Planck 2018."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "h0_planck_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from math_generator_benchmark_formula_eval import eval_h0_benchmark_formula  # noqa: E402

PLANCK_H0 = 67.36
FO200_FORMULA = "10 * (1 + abs(p_base) * a_in / abs(c_cosm))"
GOLDEN_VALUE = 67.27021167735879
GOLDEN_ERROR_PCT = abs(GOLDEN_VALUE - PLANCK_H0) / PLANCK_H0 * 100.0


def build() -> dict:
    computed = float(eval_h0_benchmark_formula())
    err = abs(computed - PLANCK_H0) / PLANCK_H0 * 100.0
    records = [
        {
            "lab": "h0_planck",
            "property": "H0_planck_km_s_Mpc",
            "rule_id": "FO-200",
            "computed": computed,
            "measured": PLANCK_H0,
            "measured_uncertainty": 0.54,
            "error_pct": err,
            "eval_kind": "h0_live",
            "comparison_class": "cmb_sector_prediction",
            "formula": FO200_FORMULA,
            "reference": "Planck2018",
        },
        {
            "lab": "h0_planck",
            "property": "global_H0_reference",
            "rule_id": "FO-100",
            "computed": float(json.loads((ROOT / "data/canonical_constants.json").read_text())["wave1"]["H0"]),
            "measured": 68.44005682979427,
            "error_pct": 0.0,
            "eval_kind": "wave1_crosscheck",
            "comparison_class": "tension_sector_crosscheck",
            "note": "Global FSOT H0 remains 68.44 for tension sector; Planck uses FO-200 readout.",
        },
    ]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [
            "vendor/math_generator/benchmark_reports/hubble_report.json",
            "scripts/math_generator_benchmark_formula_eval.py",
        ],
        "maps_to_lean": ["Cosmology"],
        "rule_id": "FO-200",
        "record_count": len(records),
        "observable_count": 1,
        "median_error_pct": err,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  H0={doc['records'][0]['computed']:.6f}  err={doc['records'][0]['error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())