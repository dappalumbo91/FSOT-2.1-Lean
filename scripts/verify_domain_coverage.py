#!/usr/bin/env python3
"""Verify 35-domain coverage report against fsot_35_domain_registry.yaml thresholds."""

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
REPORT = ROOT / "data" / "domain_coverage_report.json"


def verify() -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    ver = spec.get("verification", {})
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    issues: list[str] = []

    if report.get("domain_count", 0) < ver.get("min_domain_count", 35):
        issues.append(f"domain_count {report.get('domain_count')} < 35")
    if report.get("domains_with_empirical_data", 0) < ver.get("min_empirical_domains", 28):
        issues.append("too few domains with empirical data")
    if report.get("total_empirical_records", 0) < ver.get("min_total_empirical_records", 2000):
        issues.append("total empirical records too low")
    if report.get("lean_param_aligned_count", 0) != report.get("lean_mapped_count", 0):
        issues.append(
            f"lean override misalignment: {report.get('lean_param_aligned_count')}/"
            f"{report.get('lean_mapped_count')}"
        )
    misaligned = [
        d["neurolab_domain"]
        for d in report.get("domains", [])
        if d.get("lean_param_aligned") is False
    ]
    if misaligned:
        issues.append(f"lean override failures: {misaligned}")

    smiles_n = sum(
        1
        for d in report.get("domains", [])
        if any(s.get("lab") == "smiles_lab" for s in d.get("empirical_sources", []))
    )
    summary = {
        "domain_count": report.get("domain_count"),
        "empirical_domains": report.get("domains_with_empirical_data"),
        "total_empirical_records": report.get("total_empirical_records"),
        "lean_aligned": f"{report.get('lean_param_aligned_count')}/{report.get('lean_mapped_count')}",
        "negative_scalar_domains": len(report.get("negative_scalar_domains") or []),
        "smiles_backed_domains": smiles_n,
        "issues": len(issues),
    }
    return issues, summary


def main() -> int:
    if not REPORT.exists():
        print("FAIL: run scripts/run_domain_coverage_eval.py first")
        return 1
    issues, summary = verify()
    print("=== Domain coverage verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All domain coverage checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())