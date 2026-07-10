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
sys.path.insert(0, str(ROOT / "scripts"))
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"

from benchmark_margin_lib import analyze_benchmark  # noqa: E402


def _record_count(doc: dict) -> int:
    for key in ("record_count", "observable_count", "month_count"):
        val = doc.get(key)
        if val is not None:
            return int(val)
    records = doc.get("records") or []
    if records:
        return len(records)
    nested = 0
    for val in doc.values():
        if isinstance(val, dict):
            for key in ("record_count", "observable_count", "month_count"):
                if val.get(key) is not None:
                    nested += int(val[key])
    return nested


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = spec.get("verification") or {}
    min_records = int(ver.get("min_records_per_domain", 5))
    max_median = float(ver.get("max_median_error_pct", 0.5))
    min_classifier_acc = float(ver.get("min_classifier_accuracy_pct", 99.5))
    excluded = set(ver.get("excluded_benchmarks") or [])
    issues: list[str] = []

    for name, cfg in (spec.get("extension_domains") or {}).items():
        rel = cfg["benchmark_data"]
        if Path(rel).name in excluded:
            continue
        path = ROOT / rel
        if not path.exists():
            issues.append(f"{name}: missing {path}")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        n = _record_count(doc)
        margin = analyze_benchmark(doc, file_name=path.name)
        med = margin.get("official_pooled_median_error_pct")
        cls_acc = margin.get("classifier_accuracy_pct")
        print(
            f"  {name}: records={n} pooled={med} "
            f"classifier_acc={cls_acc if cls_acc is not None else 'n/a'}"
        )
        if n < min_records:
            issues.append(f"{name}: records {n} < {min_records}")
        if med is not None and float(med) > max_median:
            issues.append(f"{name}: pooled median {med} > {max_median}%")
        if margin.get("classifier_count", 0) > 0 and not margin.get("classifier_pass"):
            issues.append(
                f"{name}: classifier accuracy {cls_acc}% < {min_classifier_acc}%"
            )

    print("=== Extension domains verification ===")
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All extension domain checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())