#!/usr/bin/env python3
"""Ingest magnetic string lattice simulation into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "magnetic_strings_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from magnetic_strings import load_magnetic_strings, summarize_magnetic_strings  # noqa: E402


def ingest_magnetic(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    root = Path(manifest["magnetic_root"])
    json_path = root / manifest["artifacts"]["final_json"]["path"]
    data = load_magnetic_strings(json_path)
    return {"present": json_path.exists(), "data_path": str(json_path), **summarize_magnetic_strings(data)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest magnetic string lattice")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    magnetic = ingest_magnetic()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["magnetic_strings"] = magnetic
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  strings: {magnetic['string_count']}  S_em: {magnetic['S_em']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())