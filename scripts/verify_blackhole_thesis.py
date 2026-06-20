#!/usr/bin/env python3
"""Verify BlackHole thermo thesis observables."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "blackhole_thesis_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from blackhole_thesis_lab import parse_thesis_table, summarize_blackhole  # noqa: E402


def verify() -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    md = Path(manifest["thesis_root"]) / manifest["artifacts"]["thesis_md"]["path"]
    issues: list[str] = []
    if not md.exists():
        return [f"missing thesis: {md}"], {}
    live = summarize_blackhole(parse_thesis_table(md))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    if not registry.get("blackhole_thesis"):
        issues.append("blackhole_thesis: not ingested")
    if live["observable_count"] < ver.get("observable_count_min", 27):
        issues.append(f"observable_count={live['observable_count']}")
    if live["within_target_2pct"] < ver.get("within_target_2pct_min", 27):
        issues.append(f"within_2pct={live['within_target_2pct']}")
    if live["max_error_pct"] > ver.get("max_error_pct", 2.0):
        issues.append(f"max_error_pct={live['max_error_pct']}")
    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify()
    print("=== BlackHole thesis verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All BlackHole thesis checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())