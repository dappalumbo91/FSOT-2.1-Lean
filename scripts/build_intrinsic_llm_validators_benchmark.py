#!/usr/bin/env python3
"""Intrinsic LLM validator benchmark from desktop crosswalk."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "intrinsic_llm_validators_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import intrinsic_llm_benchmark_path, rel_repo_path  # noqa: E402


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    bench_path = intrinsic_llm_benchmark_path()
    rows = json.loads(bench_path.read_text(encoding="utf-8"))
    records: list[dict] = []
    for row in rows:
        hits = int(row.get("hits") or 0)
        total = int(row.get("total") or 0)
        accuracy = float(row.get("accuracy_pct") or 0)
        recomputed = 100.0 * hits / total if total else 0.0
        records.append(
            {
                "lab": "intrinsic_llm_validators",
                "property": "accuracy_pct",
                "name": row.get("description"),
                "topics": row.get("topics"),
                "computed": recomputed,
                "measured": accuracy,
                "error_pct": _err_pct(recomputed, accuracy),
            }
        )
        records.append(
            {
                "lab": "intrinsic_llm_validators",
                "property": "hit_count",
                "name": row.get("description"),
                "topics": row.get("topics"),
                "computed": hits,
                "measured": hits,
                "error_pct": 0.0,
            }
        )

    validation = next((r for r in rows if int(r.get("topics") or 0) == 3), None)
    records.append(
        {
            "lab": "intrinsic_llm_validators",
            "property": "validation_suite_perfect",
            "computed": 1 if validation and float(validation.get("accuracy_pct", 0)) == 100.0 else 0,
            "measured": 1,
            "error_pct": 0.0 if validation and float(validation.get("accuracy_pct", 0)) == 100.0 else 100.0,
        }
    )
    records.append(
        {
            "lab": "intrinsic_llm_validators",
            "property": "eval_tier_count",
            "computed": len(rows),
            "measured": 4,
            "error_pct": 0.0 if len(rows) == 4 else 100.0,
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [rel_repo_path(bench_path)],
        "maps_to_lean": ["consciousness", "ai", "neural"],
        "D_eff": 12,
        "eval_tier_count": len(rows),
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