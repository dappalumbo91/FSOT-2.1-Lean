#!/usr/bin/env python3
"""Ingest Fsot trinary OS FSOTB oracles into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "trinary_os_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from trinary_os_invariants import (  # noqa: E402
    derived_os_constants,
    load_fsotb_oracles,
    summarize_trinary_os,
)


def ingest_trinary_os(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    fsot_os_root = Path(manifest["fsot_os_root"])
    oracles = load_fsotb_oracles(fsot_os_root, manifest["artifacts"]["oracles"])
    constants = derived_os_constants()
    return {
        "present": fsot_os_root.exists() and len(oracles) >= 3,
        "fsot_os_root": str(fsot_os_root),
        **summarize_trinary_os(oracles, constants),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Fsot trinary OS oracles")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    trinary = ingest_trinary_os()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["trinary_os"] = trinary
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  oracles: {trinary['oracle_count']}")
    print(f"  seeds_hash: {trinary['constants']['seeds_hash_hex']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())