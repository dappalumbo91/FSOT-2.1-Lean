#!/usr/bin/env python3
"""Verify Tier-10 domain precision report against policy thresholds."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "data" / "fsot_35_domain_registry.yaml"
REPORT = ROOT / "data" / "domain_precision_report.json"


def verify() -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    ver = spec.get("precision_verification") or {}
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    issues: list[str] = []

    min_numeric = int(ver.get("min_domains_with_numeric_precision", 25))
    min_target = int(ver.get("min_domains_target_band", 18))
    max_huge = int(ver.get("max_huge_gap_domains", 2))
    max_unacceptable = int(ver.get("max_unacceptable_domains", 3))

    if report.get("domains_with_numeric_precision", 0) < min_numeric:
        issues.append(
            f"numeric precision domains {report.get('domains_with_numeric_precision')} < {min_numeric}"
        )
    if report.get("domains_target_band_2pct", 0) < min_target:
        issues.append(
            f"target-band domains {report.get('domains_target_band_2pct')} < {min_target}"
        )
    if report.get("domains_huge_gap", 0) > max_huge:
        issues.append(
            f"huge-gap domains {report.get('domains_huge_gap')} > {max_huge}: "
            f"{report.get('huge_gap_domains')}"
        )
    unacceptable = [
        d["neurolab_domain"]
        for d in report.get("domains", [])
        if d.get("precision_status") == "unacceptable"
    ]
    if len(unacceptable) > max_unacceptable:
        issues.append(f"unacceptable domains {unacceptable}")

    # Sign mismatches are diagnostics, not hard fails — but warn loudly.
    mismatch = report.get("sign_mismatch_domains") or []

    summary = {
        "domain_count": report.get("domain_count"),
        "numeric_precision": report.get("domains_with_numeric_precision"),
        "target_band_2pct": report.get("domains_target_band_2pct"),
        "tolerable_band_5pct": report.get("domains_tolerable_band_5pct"),
        "huge_gap": report.get("domains_huge_gap"),
        "sign_mismatch": len(mismatch),
        "issues": len(issues),
    }
    return issues, summary, mismatch


def main() -> int:
    if not REPORT.exists():
        print("FAIL: run scripts/run_domain_precision_eval.py first")
        return 1
    issues, summary, mismatch = verify()
    print("=== Domain precision verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if mismatch:
        print(f"  sign_mismatch_domains: {mismatch}")
        print("  NOTE: sign mismatches indicate param/application gaps, not Lean proof gaps.")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All domain precision checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())