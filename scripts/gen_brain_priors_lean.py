#!/usr/bin/env python3
"""
Generate FSOT/Formal/BrainPriors.lean from ingested lab_registry.json.

Certifies brain component dna_proxy genetic trinary counts against the
27-pattern codon space (3³) proved in FSOT.Formal.Genomic.

Run after ingest_lab_data.py:
  python scripts/gen_brain_priors_lean.py
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "BrainPriors.lean"


def lean_ident(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", name.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    if slug and slug[0].isdigit():
        slug = f"c_{slug}"
    return slug or "component"


def genetic_sum_prop(name: str) -> str:
    return (
        f"{name}_genetic_plus + {name}_genetic_zero + {name}_genetic_minus = "
        "brain_prior_dna_bases"
    )


def spin_sum_prop(name: str) -> str:
    return f"{name}_spin_plus + {name}_spin_minus = brain_prior_dna_bases"


def emit_theorem(name: str) -> list[str]:
    genetic_unfold = (
        f"brain_prior_dna_bases {name}_genetic_plus {name}_genetic_zero {name}_genetic_minus"
    )
    return [
        f"theorem {name}_genetic_counts_sum :",
        f"    {genetic_sum_prop(name)} := by",
        f"  unfold {genetic_unfold}; norm_num",
        "",
        f"theorem {name}_genetic_zero_is_superposition :",
        f"    ({name}_genetic_zero : ℝ) / brain_prior_dna_bases = {name}_superposition_ratio := by",
        f"  unfold {name}_superposition_ratio {name}_genetic_zero brain_prior_dna_bases; norm_num",
        "",
    ]


def emit_component_defs(row: dict, dna_bases: int) -> list[str]:
    name = lean_ident(row["component"])
    sig = row["trinary_signature"]
    lines = [
        f"/-- `{row['component']}` genetic trinary counts from dna_proxy ({dna_bases} bp). -/",
        f"def {name}_genetic_plus : ℕ := {sig['genetic_plus']}",
        f"def {name}_genetic_zero : ℕ := {sig['genetic_zero']}",
        f"def {name}_genetic_minus : ℕ := {sig['genetic_minus']}",
        f"def {name}_spin_plus : ℕ := {sig['spin_plus']}",
        f"def {name}_spin_minus : ℕ := {sig['spin_minus']}",
        (
            f"def {name}_superposition_ratio : ℝ := "
            f"({name}_genetic_zero : ℝ) / brain_prior_dna_bases"
        ),
        "",
    ]
    lines.extend(emit_theorem(name))
    lines.extend(
        [
            f"theorem {name}_spin_counts_sum :",
            f"    {spin_sum_prop(name)} := by",
            f"  unfold brain_prior_dna_bases {name}_spin_plus {name}_spin_minus; norm_num",
            "",
        ]
    )
    return lines


def build_lean(registry: dict) -> str:
    priors = registry.get("neurolab_bio", {}).get("brain_component_priors", {})
    rows = priors.get("rows", [])
    if not rows:
        raise RuntimeError("brain_component_priors missing from lab_registry.json — run ingest_lab_data.py")

    count = priors.get("count", len(rows))
    dna_bases = rows[0]["trinary_signature"]["codon_count"] * 3
    codon_count = rows[0]["trinary_signature"]["codon_count"]

    for row in rows:
        sig = row["trinary_signature"]
        if sig["codon_count"] * 3 != dna_bases:
            raise RuntimeError(f"{row['component']}: inconsistent dna/codon length")

    components = [lean_ident(r["component"]) for r in rows]
    sum_theorems = [f"{c}_genetic_counts_sum" for c in components]
    spin_theorems = [f"{c}_spin_counts_sum" for c in components]

    header = """/-
  FSOT Formal BrainPriors — auto-generated genetic trinary certificates.

  Source: data/lab_registry.json → neurolab_bio.brain_component_priors
  Generator: scripts/gen_brain_priors_lean.py

  Each brain component carries a 72bp dna_proxy. Per-base FSOT genetic trits
  (A→+1, G/C→0, T→−1) sum to 72; 24 codons each draw from the 27-pattern
  space (3³) certified in FSOT.Formal.Genomic.
-/

import FSOT.Formal.Genomic

namespace FSOT.Formal

noncomputable section

open Real

"""
    body: list[str] = [
        f"def brain_component_count : ℕ := {count}",
        f"def brain_prior_dna_bases : ℕ := {dna_bases}",
        f"def brain_prior_codon_count : ℕ := {codon_count}",
        "",
        "theorem brain_prior_codon_from_dna :",
        "    brain_prior_codon_count * 3 = brain_prior_dna_bases := by",
        "  unfold brain_prior_codon_count brain_prior_dna_bases; norm_num",
        "",
        (
            "/-- Each codon's 3-base genetic vector ranges over 3³ = 27 trinary patterns "
            "(link to Genomic Sciences). -/"
        ),
        "theorem brain_prior_codon_pattern_space_eq_twenty_seven :",
        "    genetic_trinary_alphabet_card ^ 3 = 27 :=",
        "  codon_genetic_pattern_space_eq_twenty_seven",
        "",
        (
            "/-- 64 codons map onto the 27-pattern genetic space with degeneracy 64/27. -/"
        ),
        "theorem brain_prior_codon_genetic_degeneracy :",
        "    (4 : ℝ) ^ 3 / (genetic_trinary_alphabet_card : ℝ) ^ 3 = (64 : ℝ) / 27 :=",
        "  codon_genetic_degeneracy",
        "",
    ]

    for row in rows:
        body.extend(emit_component_defs(row, dna_bases))

    bundle_props = [
        f"brain_component_count = {count}",
        f"brain_prior_dna_bases = {dna_bases}",
        f"brain_prior_codon_count = {codon_count}",
        "brain_prior_codon_count * 3 = brain_prior_dna_bases",
        "genetic_trinary_alphabet_card ^ 3 = 27",
        *[genetic_sum_prop(c) for c in components],
        *[spin_sum_prop(c) for c in components],
    ]
    bundle_proofs = [
        "by unfold brain_component_count; norm_num",
        "by unfold brain_prior_dna_bases; norm_num",
        "by unfold brain_prior_codon_count; norm_num",
        "by unfold brain_prior_codon_count brain_prior_dna_bases; norm_num",
        "brain_prior_codon_pattern_space_eq_twenty_seven",
        *sum_theorems,
        *spin_theorems,
    ]

    body.append(
        f"/-- Bundle: {count} brain components, {dna_bases}bp genetic vectors, "
        "27-pattern codon space. -/"
    )
    body.append("theorem brain_component_priors_trinary_bundle :")
    for i, prop in enumerate(bundle_props):
        conj = " ∧" if i < len(bundle_props) - 1 else " := by"
        body.append(f"    {prop}{conj}")
    body.append(f"  refine ⟨{bundle_proofs[0]}, {bundle_proofs[1]}, {bundle_proofs[2]},")
    body.append(f"    {bundle_proofs[3]}, {bundle_proofs[4]},")
    for proof in bundle_proofs[5:]:
        suffix = "," if proof != bundle_proofs[-1] else "⟩"
        body.append(f"    {proof}{suffix}")
    body.extend(["", "end", "", "end FSOT.Formal", ""])

    return header + "\n".join(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate BrainPriors.lean from lab registry")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    if not args.registry.exists():
        print(f"FAIL: missing {args.registry}")
        return 1

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    lean_src = build_lean(registry)
    args.output.write_text(lean_src, encoding="utf-8")
    count = registry["neurolab_bio"]["brain_component_priors"]["count"]
    print(f"Wrote {args.output} ({count} brain components, trinary genetic certificates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())