#!/usr/bin/env python3
"""Ingest FSOT Fuel Lab compound profiles into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "fuel_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fuel_compounds import load_profiles, summarize_fuel  # noqa: E402


def ingest_fuel(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    fuel_root = Path(manifest["fuel_root"])
    profiles = load_profiles(fuel_root)
    summary = summarize_fuel(profiles)
    return {
        "present": fuel_root.exists(),
        "fuel_root": str(fuel_root),
        "profiles": profiles,
        **summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Fuel Lab profiles")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    fuel = ingest_fuel()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["fuel_lab"] = fuel
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  profiles: {fuel['profile_count']}")
    print(f"  entries: {fuel['entry_count']} ({fuel['resolved_count']} resolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())