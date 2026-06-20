#!/usr/bin/env python3
"""
Generate FSOT/Formal/ProteinPriors.lean from lab_registry protein_formulas.

Links 20 canonical amino acid trinary phases to the 27-pattern genomic space.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "ProteinPriors.lean"


def lean_ident(letter: str) -> str:
    return {
        "A": "alanine", "R": "arginine", "N": "asparagine", "D": "aspartic_acid",
        "C": "cysteine", "Q": "glutamine", "E": "glutamic_acid", "G": "glycine",
        "H": "histidine", "I": "isoleucine", "L": "leucine", "K": "lysine",
        "M": "methionine", "F": "phenylalanine", "P": "proline", "S": "serine",
        "T": "threonine", "W": "tryptophan", "Y": "tyrosine", "V": "valine",
    }[letter]


def emit_aa_block(row: dict) -> list[str]:
    name = lean_ident(row["letter"])
    c, p, v = row["charge"], row["polarity"], row["volume"]
    return [
        f"/-- `{row['name']}` ({row['letter']}) trinary phase [Charge, Polarity, Volume]. -/",
        f"def {name}_charge : ℤ := {c}",
        f"def {name}_polarity : ℤ := {p}",
        f"def {name}_volume : ℤ := {v}",
        f"theorem {name}_trinary_phase :",
        f"    ({name}_charge, {name}_polarity, {name}_volume) = ({c}, {p}, {v}) := by",
        f"  unfold {name}_charge {name}_polarity {name}_volume; norm_num",
        "",
    ]


def build_lean(registry: dict) -> str:
    protein = registry.get("protein_formulas", {})
    rows = protein.get("rows", [])
    if len(rows) != 20:
        raise RuntimeError("protein_formulas.rows must have 20 amino acids — run ingest_protein_formulas.py")

    aa_names = [lean_ident(r["letter"]) for r in rows]
    distinct = protein.get("distinct_trinary_patterns", 0)
    count = protein.get("amino_acid_count", 20)

    header = """/-
  FSOT Formal ProteinPriors — auto-generated amino-acid trinary certificates.

  Source: Genetics/fsot_protein + data/lab_registry.json → protein_formulas
  Generator: scripts/gen_protein_priors_lean.py

  Each canonical amino acid maps to [Charge, Polarity, Volume] ∈ {-1,0,+1}³,
  a subset of the 27-pattern genomic codon space (FSOT.Formal.Genomic).
-/

import FSOT.Formal.Genomic

namespace FSOT.Formal

noncomputable section

open Real

"""
    body: list[str] = [
        f"def canonical_amino_acid_count : ℕ := {count}",
        f"def distinct_aa_trinary_patterns : ℕ := {distinct}",
        "",
        "theorem canonical_amino_acid_count_eq_twenty :",
        "    canonical_amino_acid_count = 20 := by",
        "  unfold canonical_amino_acid_count; norm_num",
        "",
        "theorem protein_trinary_pattern_space_eq_twenty_seven :",
        "    genetic_trinary_alphabet_card ^ 3 = 27 :=",
        "  codon_genetic_pattern_space_eq_twenty_seven",
        "",
        "theorem protein_amino_acid_genomic_identity :",
        "    4 * phi ^ 3 + 8 / phi ^ 2 = 20 :=",
        "  amino_acids_canonical_eq_twenty",
        "",
    ]

    for row in rows:
        body.extend(emit_aa_block(row))

    phase_props = [
        f"({lean_ident(r['letter'])}_charge, {lean_ident(r['letter'])}_polarity, "
        f"{lean_ident(r['letter'])}_volume) = ({r['charge']}, {r['polarity']}, {r['volume']})"
        for r in rows
    ]
    phase_proofs = [f"{lean_ident(r['letter'])}_trinary_phase" for r in rows]
    bundle_props = [
        "canonical_amino_acid_count = 20",
        f"distinct_aa_trinary_patterns = {distinct}",
        "distinct_aa_trinary_patterns ≤ genetic_trinary_alphabet_card ^ 3",
        "genetic_trinary_alphabet_card ^ 3 = 27",
        "4 * phi ^ 3 + 8 / phi ^ 2 = 20",
        *phase_props,
    ]
    proofs = [
        "by unfold canonical_amino_acid_count; norm_num",
        f"by unfold distinct_aa_trinary_patterns; norm_num",
        "by unfold distinct_aa_trinary_patterns genetic_trinary_alphabet_card; norm_num",
        "protein_trinary_pattern_space_eq_twenty_seven",
        "protein_amino_acid_genomic_identity",
        *phase_proofs,
    ]

    body.append("/-- Bundle: 20 amino acids, trinary phases ⊆ 27-pattern genomic space. -/")
    body.append("theorem protein_amino_acid_trinary_bundle :")
    for i, prop in enumerate(bundle_props):
        conj = " ∧" if i < len(bundle_props) - 1 else " := by"
        body.append(f"    {prop}{conj}")
    body.append(f"  refine ⟨{proofs[0]}, {proofs[1]}, {proofs[2]}, {proofs[3]}, {proofs[4]},")
    for proof in proofs[5:]:
        suffix = "," if proof != proofs[-1] else "⟩"
        body.append(f"    {proof}{suffix}")
    body.extend(["", "end", "", "end FSOT.Formal", ""])
    return header + "\n".join(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate ProteinPriors.lean from lab registry")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    if not args.registry.exists():
        print(f"FAIL: missing {args.registry}")
        return 1

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    lean_src = build_lean(registry)
    args.output.write_text(lean_src, encoding="utf-8")
    print(f"Wrote {args.output} ({registry['protein_formulas']['amino_acid_count']} amino acids)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())