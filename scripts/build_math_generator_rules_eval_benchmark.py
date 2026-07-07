#!/usr/bin/env python3
"""Math generator per-rule eval across 1520 formal rules."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "math_generator_rules_eval_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import math_generator_rules_root, rel_repo_path  # noqa: E402
from math_generator_rules_eval import evaluate_all_rules  # noqa: E402


def build() -> dict:
    rules_root = math_generator_rules_root()
    records, summary = evaluate_all_rules(rules_root)
    errs = sorted(r["error_pct"] for r in records)
    schema_fail = sum(1 for r in records if not r.get("schema_valid"))
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": rel_repo_path(rules_root),
        "maps_to_lean": ["particle", "mathematical", "consciousness"],
        "D_eff": 17,
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "schema_fail_count": schema_fail,
        **summary,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  rules: {doc['record_count']}  median_err: {doc['median_error_pct']}  "
        f"schema_fail: {doc['schema_fail_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())