#!/usr/bin/env python3
"""Ingest FSOT protein amino-acid trinary phases into lab_registry.json."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "protein_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys_path = ROOT / "scripts"
import sys

sys.path.insert(0, str(sys_path))
from protein_trinary import (  # noqa: E402
    AMINO_ACID_NAMES,
    AMINO_ACID_TRINARY,
    summarize_phases,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def ingest_protein(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    genetics_root = Path(manifest["genetics_root"])
    formulas_path = genetics_root / manifest["artifacts"]["formulas_json"]["path"]

    formulas = json.loads(formulas_path.read_text(encoding="utf-8")) if formulas_path.exists() else {}
    summary = summarize_phases()
    rows = []
    for letter in sorted(AMINO_ACID_TRINARY):
        charge, polarity, volume = AMINO_ACID_TRINARY[letter]
        rows.append({
            "letter": letter,
            "name": AMINO_ACID_NAMES[letter],
            "charge": charge,
            "polarity": polarity,
            "volume": volume,
            "pattern": f"{charge},{polarity},{volume}",
        })

    return {
        "present": formulas_path.exists(),
        "path": str(formulas_path),
        "sha256": sha256_file(formulas_path) if formulas_path.exists() else None,
        "formula_count": len(formulas.get("formulas", [])),
        "amino_acid_count": summary["amino_acid_count"],
        "distinct_trinary_patterns": summary["distinct_trinary_patterns"],
        "trinary_pattern_space": summary["pattern_space_size"],
        "rows": rows,
        "formula_ids": [f["id"] for f in formulas.get("formulas", [])],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest protein trinary phases into lab_registry.json")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    protein = ingest_protein()
    if args.registry.exists():
        registry = json.loads(args.registry.read_text(encoding="utf-8"))
    else:
        registry = {"registry_version": "1.0"}

    registry["protein_formulas"] = protein
    args.registry.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {args.registry}")
    print(f"  amino acids: {protein['amino_acid_count']}")
    print(f"  distinct trinary patterns: {protein['distinct_trinary_patterns']} / {protein['trinary_pattern_space']}")
    print(f"  formula catalog entries: {protein['formula_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())