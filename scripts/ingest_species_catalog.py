#!/usr/bin/env python3
"""Ingest FSOT Machine & Molecule species catalog into lab_registry.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "species_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from species_catalog import flatten_catalog, load_catalog, summarize_species  # noqa: E402


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def ingest_species(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    root = Path(manifest["machine_molecule_root"])
    catalog_path = root / manifest["artifacts"]["catalog_json"]["path"]
    catalog = load_catalog(catalog_path)
    rows = flatten_catalog(catalog)
    summary = summarize_species(catalog, rows)
    return {
        "present": catalog_path.exists(),
        "catalog_path": str(catalog_path),
        "catalog_sha256": sha256_file(catalog_path) if catalog_path.exists() else None,
        "rows": rows,
        **summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest species catalog")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    species = ingest_species()
    registry = json.loads(args.registry.read_text(encoding="utf-8")) if args.registry.exists() else {}
    registry["species_catalog"] = species
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  species: {species['species_count']} (metals={species['category_counts']['metals']}, molecules={species['category_counts']['molecules']}, polymers={species['category_counts']['polymers']})")
    print(f"  properties: {species['property_count']}, max error: {species['max_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())