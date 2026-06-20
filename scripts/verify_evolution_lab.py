#!/usr/bin/env python3
"""Verify FSOT biological evolution sim."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "evolution_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from evolution_lab import load_best_organism, load_operons, summarize_evolution  # noqa: E402


def verify_evolution(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    root = Path(manifest["evolution_root"])
    operons_path = root / manifest["artifacts"]["operons_json"]["path"]
    best_path = root / manifest["artifacts"]["best_organism_json"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not operons_path.exists() or not best_path.exists():
        return ["missing evolution sim artifacts"], {}

    live = summarize_evolution(load_operons(operons_path), load_best_organism(best_path))
    if not registry.get("evolution_lab"):
        issues.append("evolution_lab: not ingested — run ingest_evolution_lab.py")
    if live["operon_count"] < ver.get("operon_count_min", 13):
        issues.append(f"evolution_lab: only {live['operon_count']} operons")
    if (live.get("fitness") or 0) < ver.get("fitness_min", 50):
        issues.append(f"evolution_lab: fitness={live.get('fitness')} below minimum")
    if (live.get("biological_capacity") or 0) < ver.get("biological_capacity_min", 5000):
        issues.append("evolution_lab: biological_capacity below minimum")

    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify_evolution()
    print("=== Evolution Lab verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All evolution Lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())