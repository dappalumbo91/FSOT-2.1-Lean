#!/usr/bin/env python3
"""Ingest FSOT Trinary Fluid Computer v2 audit constants into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "trinary_fluid_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from trinary_fluid_computer import summarize_trinary_fluid  # noqa: E402


def ingest_trinary_fluid(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    trinary_root = Path(manifest["trinary_fluid_root"])
    audit_path = trinary_root / manifest["artifacts"]["audit_script"]["path"]
    return {
        "present": trinary_root.exists(),
        "trinary_fluid_root": str(trinary_root),
        "audit_script_path": str(audit_path),
        **summarize_trinary_fluid(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Trinary Fluid Computer constants")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    trinary = ingest_trinary_fluid()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["trinary_fluid_computer"] = trinary
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(
        f"  engine_accuracy: {trinary.get('engine_accuracy_pct')}%  "
        f"metatron_pathways: {trinary.get('metatron_pathways')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())