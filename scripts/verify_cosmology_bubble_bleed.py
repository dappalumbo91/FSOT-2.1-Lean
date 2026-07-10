#!/usr/bin/env python3
"""Verify cosmology bubble-bleed lab benchmarks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cosmology_bubble_bleed_manifest.yaml"
BENCH = ROOT / "data" / "cosmology_bubble_bleed_benchmark.json"


def verify() -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    issues: list[str] = []
    if not BENCH.exists():
        return [f"missing benchmark: {BENCH}"], {}
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    if bench.get("nebula_count", 0) < ver.get("min_nebula_records", 15):
        issues.append(f"nebula_count={bench.get('nebula_count')}")
    if bench.get("frb_count", 0) < ver.get("min_frb_records", 20):
        issues.append(f"frb_count={bench.get('frb_count')}")
    if bench.get("h0_sector_count", 0) < ver.get("min_h0_sector_records", 4):
        issues.append(f"h0_sector_count={bench.get('h0_sector_count')}")
    neb_rate = float(bench.get("nebula_match_rate") or 0.0)
    if neb_rate < ver.get("min_nebula_coupling_match_rate", 0.55):
        issues.append(f"nebula_coupling_match_rate={neb_rate:.3f}")
    fw_rate = float(bench.get("nebula_framework_fit_rate") or 0.0)
    if fw_rate < ver.get("min_framework_fit_rate", 1.0):
        issues.append(f"nebula_framework_fit_rate={fw_rate:.3f}")
    wh_rate = float(bench.get("nebula_wh_closure_match_rate") or 0.0)
    if wh_rate < ver.get("min_wh_closure_match_rate", 1.0):
        issues.append(f"nebula_wh_closure_match_rate={wh_rate:.3f}")
    bh_rate = float(bench.get("bh_spin_closure_match_rate") or 0.0)
    if bh_rate < ver.get("min_bh_spin_closure_match_rate", 1.0):
        issues.append(f"bh_spin_closure_match_rate={bh_rate:.3f}")
    frb_rate = float(bench.get("frb_classifier_match_rate") or 0.0)
    if frb_rate < ver.get("min_frb_classifier_match_rate", 0.65):
        issues.append(f"frb_classifier_match_rate={frb_rate:.3f}")
    frb_fp_rate = float(bench.get("frb_classifier_fp_rate") or 0.0)
    if frb_fp_rate > ver.get("max_frb_classifier_fp_rate", 0.05):
        issues.append(f"frb_classifier_fp_rate={frb_fp_rate:.3f}")
    med = bench.get("median_error_pct")
    if med is not None and float(med) > ver.get("max_median_error_pct", 5.0):
        issues.append(f"median_error_pct={med}")
    h0_errs = [
        float(r["error_pct"])
        for r in bench.get("records") or []
        if r.get("property") == "sector_h0_overlay"
    ]
    if h0_errs and max(h0_errs) > ver.get("max_sector_h0_error_pct", 8.0):
        issues.append(f"max_sector_h0_error_pct={max(h0_errs):.3f}")
    return issues, {**bench, "issues": len(issues)}


def main() -> int:
    issues, summary = verify()
    print("=== Cosmology bubble bleed verification ===")
    for k in (
        "nebula_count",
        "frb_count",
        "h0_sector_count",
        "observable_count",
        "nebula_framework_fit_rate",
        "nebula_wh_closure_match_rate",
        "bh_spin_closure_match_rate",
        "nebula_match_rate",
        "frb_classifier_match_rate",
        "frb_classifier_fp_rate",
        "median_error_pct",
        "bubble_bleed_fraction",
        "observability",
    ):
        if k in summary:
            print(f"  {k}: {summary[k]}")
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All bubble bleed checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())