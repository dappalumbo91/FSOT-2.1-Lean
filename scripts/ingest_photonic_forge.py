#!/usr/bin/env python3
"""Ingest FSOT Photonic V2 VRAM payload into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "photonic_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from photonic_forge import load_vram_payload, photonic_constants, summarize_photonic  # noqa: E402


def ingest_photonic(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    photonic_root = Path(manifest["photonic_root"])
    payload_path = photonic_root / manifest["artifacts"]["vram_payload"]
    voxels = load_vram_payload(payload_path) if payload_path.exists() else []
    return {
        "present": payload_path.exists(),
        "photonic_root": str(photonic_root),
        "payload_path": str(payload_path),
        "constants": photonic_constants(),
        **summarize_photonic(voxels),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest FSOT Photonic V2 payload")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    photonic = ingest_photonic()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["photonic_forge"] = photonic
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  voxels: {photonic['voxel_count']}")
    print(f"  trinary counts: {photonic['trinary_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())