#!/usr/bin/env python3
"""Verify FSOT protein amino-acid trinary phases against Genetics source + registry."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "protein_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from protein_trinary import (  # noqa: E402
    AMINO_ACID_NAMES,
    AMINO_ACID_TRINARY,
    VALID_TRITS,
    pattern_key,
    summarize_phases,
)


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def check_registry_protein(registry: dict, manifest: dict) -> list[str]:
    issues: list[str] = []
    ver = manifest.get("verification", {})
    expected_aa = ver.get("amino_acid_count", 20)
    pattern_space = ver.get("trinary_pattern_space", 27)
    tol = ver.get("coordinate_tolerance", 0)

    protein = registry.get("protein_formulas", {})
    if not protein:
        return ["protein_formulas: not ingested into lab_registry.json — run ingest_protein_formulas.py"]

    if protein.get("amino_acid_count") != expected_aa:
        issues.append(
            f"protein_formulas: amino_acid_count={protein.get('amino_acid_count')} != {expected_aa}"
        )
    if protein.get("trinary_pattern_space") != pattern_space:
        issues.append(
            f"protein_formulas: trinary_pattern_space={protein.get('trinary_pattern_space')} != {pattern_space}"
        )

    summary = summarize_phases()
    if protein.get("distinct_trinary_patterns") != summary["distinct_trinary_patterns"]:
        issues.append(
            f"protein_formulas: distinct_trinary_patterns={protein.get('distinct_trinary_patterns')} "
            f"!= source {summary['distinct_trinary_patterns']}"
        )
    if summary["distinct_trinary_patterns"] > pattern_space:
        issues.append(
            f"protein trinary: distinct patterns {summary['distinct_trinary_patterns']} > {pattern_space}"
        )

    rows = protein.get("rows", [])
    if len(rows) != expected_aa:
        issues.append(f"protein_formulas: row count {len(rows)} != {expected_aa}")

    for row in rows:
        letter = row.get("letter", "?")
        if letter not in AMINO_ACID_TRINARY:
            issues.append(f"protein_formulas {letter}: unknown amino acid letter")
            continue
        expected = AMINO_ACID_TRINARY[letter]
        actual = (row.get("charge"), row.get("polarity"), row.get("volume"))
        if actual != expected:
            issues.append(
                f"protein_formulas {letter}: phase {actual} != source {expected}"
            )
        for coord, val in zip(("charge", "polarity", "volume"), actual):
            if val not in VALID_TRITS:
                issues.append(f"protein_formulas {letter}: {coord}={val} not in {{-1,0,+1}}")
            if tol == 0 and row.get(coord) != val:
                issues.append(
                    f"protein_formulas {letter}: registry {coord}={row.get(coord)} != {val}"
                )
        if row.get("name") != AMINO_ACID_NAMES[letter]:
            issues.append(
                f"protein_formulas {letter}: name={row.get('name')} != {AMINO_ACID_NAMES[letter]}"
            )
        if row.get("pattern") != pattern_key(expected):
            issues.append(
                f"protein_formulas {letter}: pattern={row.get('pattern')} != {pattern_key(expected)}"
            )

    return issues


def check_formulas_catalog(manifest: dict) -> list[str]:
    issues: list[str] = []
    genetics_root = Path(manifest["genetics_root"])
    formulas_path = genetics_root / manifest["artifacts"]["formulas_json"]["path"]
    if not formulas_path.exists():
        return [f"missing protein formulas JSON: {formulas_path}"]

    formulas = json.loads(formulas_path.read_text(encoding="utf-8"))
    entries = formulas.get("formulas", [])
    if not entries:
        issues.append("protein formulas JSON: empty formulas list")
    ids = {f.get("id") for f in entries}
    if None in ids:
        issues.append("protein formulas JSON: entry missing id")
    if len(ids) != len(entries):
        issues.append("protein formulas JSON: duplicate formula ids")
    return issues


def verify_protein(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}

    issues: list[str] = []
    issues.extend(check_formulas_catalog(manifest))
    issues.extend(check_registry_protein(registry, manifest))

    protein = registry.get("protein_formulas", {})
    summary = {
        "amino_acid_count": protein.get("amino_acid_count", 0),
        "distinct_trinary_patterns": protein.get("distinct_trinary_patterns", 0),
        "trinary_pattern_space": protein.get("trinary_pattern_space", 27),
        "formula_count": protein.get("formula_count", 0),
        "issues": len(issues),
    }
    return issues, summary


def main() -> int:
    issues, summary = verify_protein()
    print("=== Protein formula verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All protein formula checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())