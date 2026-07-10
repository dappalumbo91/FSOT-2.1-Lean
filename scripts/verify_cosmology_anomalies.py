#!/usr/bin/env python3
"""Verify cosmology anomalies benchmark."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cosmology_anomalies_manifest.yaml"
BENCH = ROOT / "data" / "cosmology_anomalies_benchmark.json"


def verify() -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    issues: list[str] = []
    if not BENCH.exists():
        return [f"missing benchmark: {BENCH}"], {}
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    if bench.get("record_count", 0) < ver.get("min_anomaly_records", 10):
        issues.append(f"record_count={bench.get('record_count')}")
    resolved = float(bench.get("resolved_fraction") or 0.0)
    if resolved < ver.get("min_resolved_fraction", 0.65):
        issues.append(f"resolved_fraction={resolved:.3f}")
    med = bench.get("median_error_pct")
    if med is not None and float(med) > ver.get("max_median_error_pct", 15.0):
        issues.append(f"median_error_pct={med}")
    return issues, bench


def main() -> int:
    issues, bench = verify()
    print("=== Cosmology anomalies verification ===")
    for k in ("record_count", "resolved_fraction", "median_error_pct", "max_error_pct"):
        if k in bench:
            print(f"  {k}: {bench[k]}")
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All anomaly checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())