#!/usr/bin/env python3
"""FSOT prediction re-derivation arc benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "prediction_rederivation_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import prediction_rederivation_summary_path, rel_repo_path  # noqa: E402


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    summary = json.loads(prediction_rederivation_summary_path().read_text(encoding="utf-8"))
    records: list[dict] = []

    for key, expected in (
        ("total_unique_predictions", 66),
        ("category_a_direct_engine", 15),
        ("category_b_derived", 51),
        ("confirmed_by_observation", 11),
        ("computable_error_pairs", 18),
        ("stabilized_improved_or_matched", 13),
    ):
        val = int(summary.get(key) or 0)
        records.append(
            {
                "lab": "prediction_rederivation",
                "property": key,
                "computed": val,
                "measured": expected,
                "error_pct": 0.0 if val == expected else _err_pct(val, expected),
            }
        )

    rate = float(summary.get("stabilized_improvement_rate_pct") or 0)
    records.append(
        {
            "lab": "prediction_rederivation",
            "property": "stabilized_improvement_rate_pct",
            "computed": rate,
            "measured": 72.2,
            "error_pct": _err_pct(rate, 72.2),
        }
    )
    records.append(
        {
            "lab": "prediction_rederivation",
            "property": "free_parameters_zero",
            "computed": 1 if summary.get("free_parameters", 1) == 0 else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("free_parameters", 1) == 0 else 100.0,
        }
    )
    records.append(
        {
            "lab": "prediction_rederivation",
            "property": "dwarf_core_radius_resolved",
            "computed": 1 if summary.get("dwarf_core_radius_resolved") else 0,
            "measured": 1,
            "error_pct": 0.0 if summary.get("dwarf_core_radius_resolved") else 100.0,
        }
    )
    records.append(
        {
            "lab": "prediction_rederivation",
            "property": "dwarf_core_radius_error_pct",
            "computed": float(summary.get("dwarf_core_radius_error_pct") or 0),
            "measured": 0.33,
            "error_pct": _err_pct(float(summary.get("dwarf_core_radius_error_pct") or 0), 0.33),
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(prediction_rederivation_summary_path())],
        "maps_to_lean": ["cosmological", "particle", "galactic"],
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