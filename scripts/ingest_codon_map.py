#!/usr/bin/env python3
"""Ingest FSOT 64-codon dual-axis trinary map into lab_registry.json."""

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
MANIFEST_PATH = ROOT / "data" / "codon_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from codon_trinary import all_codons, load_map_file, summarize_codons  # noqa: E402


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def ingest_codon(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    genetics_root = Path(manifest["genetics_root"])
    map_path = genetics_root / manifest["artifacts"]["codon_map_txt"]["path"]
    core_path = genetics_root / manifest["artifacts"]["codon_core"]["path"]
    project_root = Path(manifest["artifacts"]["build_script"]["project_root"])
    build_path = project_root / manifest["artifacts"]["build_script"]["path"]

    rows = all_codons()
    summary = summarize_codons(rows)
    file_map = load_map_file(map_path) if map_path.exists() else {}

    return {
        "present": map_path.exists(),
        "map_path": str(map_path),
        "map_sha256": sha256_file(map_path) if map_path.exists() else None,
        "codon_core_path": str(core_path),
        "codon_core_sha256": sha256_file(core_path) if core_path.exists() else None,
        "build_script_path": str(build_path),
        "build_script_sha256": sha256_file(build_path) if build_path.exists() else None,
        "file_map_rows": len(file_map),
        **summary,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest 64-codon trinary map into lab_registry.json")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    codon = ingest_codon()
    if args.registry.exists():
        registry = json.loads(args.registry.read_text(encoding="utf-8"))
    else:
        registry = {"registry_version": "1.0"}

    registry["codon_trinary_map"] = codon
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  codons: {codon['codon_count']}")
    print(
        f"  primary patterns: {codon['distinct_primary_patterns']} / {codon['primary_pattern_space']}"
    )
    print(
        f"  secondary patterns: {codon['distinct_secondary_patterns']} / "
        f"{codon['secondary_pattern_space']}"
    )
    print(f"  stop codons: {codon['stop_codon_count']} ({', '.join(codon['stop_codons'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())