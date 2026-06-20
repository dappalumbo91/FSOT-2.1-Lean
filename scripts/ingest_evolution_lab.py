#!/usr/bin/env python3
"""Ingest FSOT evolution sim into lab_registry.json."""

from __future__ import annotations

import argparse
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


def ingest_evolution(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    root = Path(manifest["evolution_root"])
    operons_path = root / manifest["artifacts"]["operons_json"]["path"]
    best_path = root / manifest["artifacts"]["best_organism_json"]["path"]
    operons = load_operons(operons_path)
    best = load_best_organism(best_path)
    return {
        "present": operons_path.exists() and best_path.exists(),
        "operons_path": str(operons_path),
        "best_path": str(best_path),
        **summarize_evolution(operons, best),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest evolution sim")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    evolution = ingest_evolution()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["evolution_lab"] = evolution
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  operons: {evolution['operon_count']}  fitness: {evolution['fitness']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())