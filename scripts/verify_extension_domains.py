#!/usr/bin/env python3
"""Verify extension domains #37-39 benchmarks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = spec.get("verification") or {}
    min_records = int(ver.get("min_records_per_domain", 5))
    max_median = float(ver.get("max_median_error_pct", 5.0))
    issues: list[str] = []

    for name, cfg in (spec.get("extension_domains") or {}).items():
        path = ROOT / cfg["benchmark_data"]
        if not path.exists():
            issues.append(f"{name}: missing {path}")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        n = doc.get("record_count") or doc.get("month_count") or len(doc.get("records") or [])
        med = doc.get("median_error_pct")
        print(f"  {name}: records={n} median_err={med}")
        if n < min_records:
            issues.append(f"{name}: records {n} < {min_records}")
        if med is not None and float(med) > max_median:
            issues.append(f"{name}: median {med} > {max_median}%")

    print("=== Extension domains verification ===")
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All extension domain checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())