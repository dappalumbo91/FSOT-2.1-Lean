#!/usr/bin/env python3
"""Verify Tier-11 Intelligence Compression ingest."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "intelligence_compression_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = manifest.get("verification") or {}
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    fic = registry.get("intelligence_compression", {})
    issues: list[str] = []

    if not fic:
        issues.append("intelligence_compression: not ingested")

    min_rows = int(ver.get("min_sweep_rows", 100))
    if fic.get("sweep_row_count", 0) < min_rows:
        issues.append(f"sweep rows {fic.get('sweep_row_count')} < {min_rows}")

    min_fertile = int(ver.get("min_fertile_rows", 5))
    if fic.get("fertile_count", 0) < min_fertile:
        issues.append(f"fertile rows {fic.get('fertile_count')} < {min_fertile}")

    min_best = float(ver.get("min_best_intelligence_score", 0.5))
    if fic.get("best_intelligence_score", 0.0) < min_best:
        issues.append(f"best intelligence score {fic.get('best_intelligence_score')} < {min_best}")

    if ver.get("optimal_must_be_fertile") and not fic.get("optimal_fertile"):
        issues.append("optimal params not in fertile window")

    print("=== Intelligence Compression verification ===")
    print(f"  sweep_rows: {fic.get('sweep_row_count')}")
    print(f"  fertile: {fic.get('fertile_count')}")
    print(f"  best_score: {fic.get('best_intelligence_score')}")
    print(f"  optimal_S: {fic.get('optimal_S_final')}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Intelligence Compression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())