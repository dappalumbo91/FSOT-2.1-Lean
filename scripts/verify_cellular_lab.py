#!/usr/bin/env python3
"""Verify cellular lab (Soul Simulator + evolution)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cellular_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cellular_lab import load_soul_manifest, summarize_cellular  # noqa: E402


def verify() -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    soul_path = Path(manifest["artifacts"]["soul_simulator_manifest"]["path"])
    operons_path = Path(manifest["artifacts"]["evolution_operons"]["path"])
    issues: list[str] = []
    if not soul_path.exists():
        issues.append(f"missing soul manifest: {soul_path}")
    if not operons_path.exists():
        issues.append(f"missing operons: {operons_path}")
    if issues:
        return issues, {}
    live = summarize_cellular(load_soul_manifest(soul_path), operons_path)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    if not registry.get("cellular_lab"):
        issues.append("cellular_lab: not ingested")
    if live["soul_records_processed"] < ver.get("soul_records_min", 200000):
        issues.append(f"soul_records={live['soul_records_processed']}")
    if live["evolution_operon_count"] < ver.get("evolution_operon_count_min", 13):
        issues.append(f"operons={live['evolution_operon_count']}")
    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify()
    print("=== Cellular lab verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All cellular lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())