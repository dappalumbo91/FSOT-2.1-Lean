#!/usr/bin/env python3
"""Verify FSOT SOTA competitiveness report against manifest thresholds."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "sota_competitiveness_manifest.yaml"
REPORT = ROOT / "data" / "sota_competitiveness_report.json"


def verify() -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = spec.get("verification", {})
    issues: list[str] = []
    if not REPORT.exists():
        return [f"missing report: {REPORT}"], {}
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    compared = int(report.get("domains_compared") or 0)
    if compared < ver.get("min_domain_comparisons", 30):
        issues.append(f"domains_compared={compared}")
    meets_frac = float(report.get("meets_or_beats_sota_fraction") or 0.0)
    if meets_frac < ver.get("min_beats_or_meets_sota_fraction", 0.85):
        issues.append(f"meets_or_beats_sota_fraction={meets_frac:.3f}")
    beats_frac = float(report.get("beats_sota_fraction") or 0.0)
    if beats_frac < ver.get("min_strict_beats_sota_fraction", 0.70):
        issues.append(f"beats_sota_fraction={beats_frac:.3f}")
    below = report.get("below_sota_domains") or []
    if len(below) > ver.get("max_below_sota_domains", 5):
        issues.append(f"below_sota_domains={below}")
    if ver.get("require_zero_free_parameters") and report.get("fsot_free_parameters") != 0:
        issues.append(f"fsot_free_parameters={report.get('fsot_free_parameters')}")
    return issues, report


def main() -> int:
    issues, report = verify()
    print("=== SOTA competitiveness verification ===")
    for k in (
        "domains_compared",
        "domains_beats_sota",
        "domains_meets_or_beats_sota",
        "beats_sota_fraction",
        "meets_or_beats_sota_fraction",
        "average_margin_vs_sota_pct",
        "fsot_free_parameters",
    ):
        if k in report:
            v = report[k]
            if isinstance(v, float) and k.endswith("_fraction"):
                print(f"  {k}: {v:.3f}")
            else:
                print(f"  {k}: {v}")
    if report.get("below_sota_domains"):
        print(f"  below_sota_domains: {report['below_sota_domains']}")
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All SOTA competitiveness checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())