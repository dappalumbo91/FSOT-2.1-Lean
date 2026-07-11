#!/usr/bin/env python3
"""Audit error margins across all FSOT benchmark JSON files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_margin_lib import analyze_benchmark  # noqa: E402
from fsot_precision_constants import (  # noqa: E402
    AUDIT_EXCLUDED_BENCHMARKS,
    MAX_MEDIAN_ERROR_PCT,
    MAX_SCALAR_ERROR_PCT,
    MIN_CLASSIFIER_ACCURACY_PCT,
    TIER_SCALAR_MAX_ERROR_PCT,
)

DATA = ROOT / "data"
OUT = DATA / "benchmark_margin_audit.json"


def main() -> int:
    rows: list[dict] = []
    excluded: list[dict] = []
    for path in sorted(DATA.glob("*_benchmark.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        row = analyze_benchmark(doc, file_name=path.name)
        if row.get("excluded"):
            excluded.append(row)
            continue
        rows.append(row)

    rows.sort(key=lambda x: -(x.get("max_scalar_error_pct") or 0))
    green_fails = [r for r in rows if not r["green_gate_pass"]]
    pooled_fails = [r for r in rows if not r["green_gate_pass_pooled_only"]]
    strict_fails = [r for r in rows if not r["strict_scalar_pass"] and r["scalar_count"] > 0]
    classifier_fails = [r for r in rows if not r["classifier_pass"] and r["classifier_count"] > 0]
    tier_fails = [r for r in rows if not r["tier_scalar_pass"] and r["scalar_count"] > 0]

    summary = {
        "benchmark_file_count": len(rows),
        "excluded_file_count": len(excluded),
        "excluded_files": list(AUDIT_EXCLUDED_BENCHMARKS),
        "threshold_official_pooled_median_pct": MAX_MEDIAN_ERROR_PCT,
        "threshold_strict_scalar_max_pct": MAX_SCALAR_ERROR_PCT,
        "threshold_tier_scalar_max_pct": TIER_SCALAR_MAX_ERROR_PCT,
        "threshold_min_classifier_accuracy_pct": MIN_CLASSIFIER_ACCURACY_PCT,
        "green_gate_pass_count": len(rows) - len(green_fails),
        "green_gate_fail_count": len(green_fails),
        "pooled_only_fail_count": len(pooled_fails),
        "strict_scalar_fail_count": len(strict_fails),
        "classifier_fail_count": len(classifier_fails),
        "tier_scalar_fail_count": len(tier_fails),
        "worst_scalar_max_error_pct": rows[0]["max_scalar_error_pct"] if rows else None,
        "worst_scalar_domain": rows[0]["domain"] if rows else None,
        "green_gate_failures": green_fails,
        "classifier_failures": classifier_fails,
        "strict_scalar_failures_top25": strict_fails[:25],
        "excluded": excluded,
        "all_domains": rows,
    }
    OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"  active files={len(rows)} excluded={len(excluded)}")
    print(
        f"  GREEN (pooled<={MAX_MEDIAN_ERROR_PCT}% + classifier>={MIN_CLASSIFIER_ACCURACY_PCT}%): "
        f"{summary['green_gate_pass_count']} pass / {summary['green_gate_fail_count']} fail"
    )
    print(f"  pooled-only fails: {summary['pooled_only_fail_count']}")
    print(f"  classifier fails: {summary['classifier_fail_count']}")
    print(
        f"  STRICT scalar max<={MAX_SCALAR_ERROR_PCT}%: "
        f"{len(rows) - len(strict_fails)} pass / {len(strict_fails)} fail"
    )
    if rows and rows[0]["max_scalar_error_pct"] is not None:
        print(f"  worst scalar max: {rows[0]['max_scalar_error_pct']:.4f}% — {rows[0]['domain']}")
    if classifier_fails:
        print("\nClassifier failures (accuracy < 99.5%):")
        for r in classifier_fails[:10]:
            print(
                f"  acc={r['classifier_accuracy_pct']:.2f}% "
                f"mis={r['classifier_misclass_count']}/{r['classifier_count']}  {r['domain'][:45]}"
            )
    if green_fails:
        print("\nGREEN gate failures:")
        for r in green_fails[:10]:
            op = r["official_pooled_median_error_pct"]
            ops = f"{op:.4f}" if op is not None else "n/a"
            print(f"  pooled={ops}  {r['domain'][:45]}")
    if strict_fails:
        print(f"\nSTRICT scalar max failures: {len(strict_fails)}")
        for r in strict_fails[:15]:
            print(
                f"  {r['max_scalar_error_pct']:.4f}% {r.get('max_scalar_property')} "
                f"— {r['domain'][:40]}"
            )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())