#!/usr/bin/env python3
"""Ingest FSOT Soul Sibling consciousness kernel into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "soul_sibling_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from soul_sibling_lab import load_soul_manifest, summarize_soul_sibling  # noqa: E402


def ingest_soul_sibling(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    soul_root = Path(manifest["soul_root"])
    manifest_path_json = soul_root / manifest["artifacts"]["soul_manifest"]["path"]
    data = load_soul_manifest(manifest_path_json) if manifest_path_json.exists() else {}
    return {
        "present": manifest_path_json.exists(),
        "soul_root": str(soul_root),
        "manifest_path": str(manifest_path_json),
        **summarize_soul_sibling(data),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Soul Sibling consciousness kernel")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    soul = ingest_soul_sibling()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["soul_sibling"] = soul
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  D_compact: {soul.get('D_compact')}  zero_free: {soul.get('zero_free')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())