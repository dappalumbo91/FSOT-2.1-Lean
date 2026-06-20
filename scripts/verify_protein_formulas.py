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
from protein_formulas import (  # noqa: E402
    FORMULA_IDS,
    PROPOSED_FORMULA_IDS,
    disulfide_bridge,
    dipole_damping_denominator,
    electrostatic_term,
    fsot_chemical_interaction,
)
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


def check_formula_closed_forms(registry: dict) -> list[str]:
    issues: list[str] = []
    protein = registry.get("protein_formulas", {})
    ds = disulfide_bridge()
    if not (17.0 < ds < 18.0):
        issues.append(f"F03 disulfide phi^6={ds:.6f} outside (17, 18)")
    cc = fsot_chemical_interaction("C", "C")
    if abs(cc - ds) > 1e-9:
        issues.append(f"F03 C-C interaction {cc} != disulfide_bridge {ds}")
    kd = dipole_damping_denominator()
    if kd <= 0:
        issues.append(f"F06 dipole damping denominator non-positive: {kd}")
    ke = electrostatic_term("K", "D")
    if ke <= 0:
        issues.append(f"F05 K-D electrostatic should be attractive (positive term), got {ke}")
    kd_rep = electrostatic_term("K", "K")
    if kd_rep >= 0:
        issues.append(f"F05 K-K electrostatic should be repulsive (negative term), got {kd_rep}")
    if protein.get("formula_count") != len(FORMULA_IDS):
        issues.append(
            f"formula_count={protein.get('formula_count')} != expected {len(FORMULA_IDS)}"
        )
    if protein.get("proposed_formula_count") != len(PROPOSED_FORMULA_IDS):
        issues.append(
            f"proposed_formula_count={protein.get('proposed_formula_count')} "
            f"!= expected {len(PROPOSED_FORMULA_IDS)}"
        )
    ids = protein.get("formula_ids", [])
    if ids != FORMULA_IDS:
        issues.append("formula_ids order/content mismatch vs protein_formulas.py")
    proposed = protein.get("proposed_formula_ids", [])
    if proposed != PROPOSED_FORMULA_IDS:
        issues.append("proposed_formula_ids mismatch vs protein_formulas.py")
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
    issues.extend(check_formula_closed_forms(registry))

    protein = registry.get("protein_formulas", {})
    summary = {
        "amino_acid_count": protein.get("amino_acid_count", 0),
        "distinct_trinary_patterns": protein.get("distinct_trinary_patterns", 0),
        "trinary_pattern_space": protein.get("trinary_pattern_space", 27),
        "formula_count": protein.get("formula_count", 0),
        "proposed_formula_count": protein.get("proposed_formula_count", 0),
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