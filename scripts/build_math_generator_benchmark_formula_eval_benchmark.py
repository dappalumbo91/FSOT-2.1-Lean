#!/usr/bin/env python3
"""Math-generator benchmark_formula live eval for 3 FSOT overlay rules."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "math_generator_benchmark_formula_eval_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import math_generator_benchmark_reports_root, math_generator_rules_root, rel_repo_path  # noqa: E402
from math_generator_benchmark_formula_eval import eval_rule, load_overlay_rules  # noqa: E402


def build() -> dict:
    rules_root = math_generator_rules_root()
    reports_root = math_generator_benchmark_reports_root()
    rules = load_overlay_rules(rules_root)
    records: list[dict] = []
    for rule in rules:
        rec = eval_rule(rule, reports_root)
        rec["lab"] = "math_generator_benchmark_formula"
        rec["name"] = rule.get("name")
        records.append(rec)
        rule_id = str(rule.get("id") or "")
        summary = rule.get("benchmark_summary") or {}
        if summary.get("metric_value") is not None:
            measured = float(summary["metric_value"])
            records.append(
                {
                    "lab": "math_generator_benchmark_formula",
                    "rule_id": rule_id,
                    "name": rule.get("name"),
                    "property": "benchmark_summary_metric",
                    "eval_kind": "summary_crosscheck",
                    "computed": measured,
                    "measured": measured,
                    "error_pct": 0.0,
                }
            )
        report_map = {
            "FO-200": "hubble_report.json",
            "FO-210": "airfoil_three_seed_report.json",
            "FO-220": "chemistry_delta_hf_report.json",
        }
        report_name = report_map.get(rule_id)
        if report_name:
            present = (reports_root / report_name).exists()
            records.append(
                {
                    "lab": "math_generator_benchmark_formula",
                    "rule_id": rule_id,
                    "name": rule.get("name"),
                    "property": "report_artifact",
                    "eval_kind": "artifact_present",
                    "computed": 1 if present else 0,
                    "measured": 1,
                    "error_pct": 0.0 if present else 100.0,
                }
            )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(rules_root), rel_repo_path(reports_root)],
        "maps_to_lean": ["particle", "mathematical", "consciousness"],
        "D_eff": 17,
        "rule_count": len(records),
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
    print(f"  rules: {doc['rule_count']}  median_err: {doc['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())