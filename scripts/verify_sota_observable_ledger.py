#!/usr/bin/env python3
"""Verify SOTA ledger: external baselines only for headline beats; fail on below-SOTA."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_sota_observable_ledger import build  # noqa: E402

LEDGER = ROOT / "data" / "sota_observable_ledger.yaml"
REPORT = ROOT / "data" / "sota_observable_ledger_report.json"


def main() -> int:
    report = build(LEDGER)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    issues: list[str] = []
    headline_records = [
        r
        for r in report.get("records") or []
        if not r.get("exclude_from_headline_beats")
        and r.get("comparison_class", "external_observable") == "external_observable"
    ]
    below = [r["id"] for r in headline_records if r.get("status") == "below_sota"]
    internal = [
        r["id"]
        for r in report.get("records") or []
        if r.get("comparison_class") == "internal_pipeline_metric"
    ]
    structural_only = [
        r["id"]
        for r in headline_records
        if r.get("status") == "structural_only" and r.get("fsot_source")
    ]

    if below:
        issues.append(f"below external SOTA: {below}")
    if structural_only:
        issues.append(
            f"headline-eligible observables missing live FSOT error: {structural_only[:10]}"
            + (f" (+{len(structural_only) - 10} more)" if len(structural_only) > 10 else "")
        )

    headline_beats = sum(
        1 for r in headline_records if r.get("status") in ("beats_sota", "meets_sota")
    )
    print("=== SOTA observable ledger verification ===")
    print(f"  total observables: {report.get('observable_count')}")
    print(f"  headline-eligible: {len(headline_records)}")
    print(f"  internal_pipeline_metric (excluded): {len(internal)}")
    print(f"  headline beats/meets: {headline_beats}")
    if below:
        print(f"  below SOTA: {below}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All SOTA ledger checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())