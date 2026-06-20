#!/usr/bin/env python3
"""
Generate FSOT/Formal/CodonPriors.lean from lab_registry codon_trinary_map.

Dual-axis encoding matches Genetics/codon_core and genomic_trinary.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "CodonPriors.lean"

ANCHOR_CODONS = ("AAA", "TTT", "GCA", "CGT", "ATG", "TAA")


def emit_codon_block(row: dict) -> list[str]:
    name = row["codon"].lower()
    p = row["primary"]
    s = row["secondary"]
    return [
        f"/-- `{row['codon']}` primary spin axis [A,G=+1; C,T=-1]. -/",
        f"def codon_{name}_primary_0 : ℤ := {p[0]}",
        f"def codon_{name}_primary_1 : ℤ := {p[1]}",
        f"def codon_{name}_primary_2 : ℤ := {p[2]}",
        f"theorem codon_{name}_primary_phase :",
        f"    (codon_{name}_primary_0, codon_{name}_primary_1, codon_{name}_primary_2) = ({p[0]}, {p[1]}, {p[2]}) := by",
        f"  unfold codon_{name}_primary_0 codon_{name}_primary_1 codon_{name}_primary_2; norm_num",
        f"/-- `{row['codon']}` secondary genetic axis [A=+1; T=-1; G,C=0]. -/",
        f"def codon_{name}_secondary_0 : ℤ := {s[0]}",
        f"def codon_{name}_secondary_1 : ℤ := {s[1]}",
        f"def codon_{name}_secondary_2 : ℤ := {s[2]}",
        f"theorem codon_{name}_secondary_phase :",
        f"    (codon_{name}_secondary_0, codon_{name}_secondary_1, codon_{name}_secondary_2) = ({s[0]}, {s[1]}, {s[2]}) := by",
        f"  unfold codon_{name}_secondary_0 codon_{name}_secondary_1 codon_{name}_secondary_2; norm_num",
        "",
    ]


def build_lean(registry: dict) -> str:
    codon = registry.get("codon_trinary_map", {})
    rows = codon.get("rows", [])
    if len(rows) != 64:
        raise RuntimeError("codon_trinary_map.rows must have 64 codons — run ingest_codon_map.py")

    distinct_p = codon.get("distinct_primary_patterns", 8)
    distinct_s = codon.get("distinct_secondary_patterns", 27)
    stop_count = codon.get("stop_codon_count", 3)
    row_by_codon = {r["codon"]: r for r in rows}

    header = """/-
  FSOT Formal CodonPriors — auto-generated 64-codon dual-axis trinary certificates.

  Source: Genetics/64_codon_trinary_map.txt + codon_core + data/lab_registry.json
  Generator: scripts/gen_codon_priors_lean.py

  primary   (spin):     A,G = +1 ; C,T = -1   — matches genomic_trinary.SPIN_MAP
  secondary (genetic):  A = +1 ; T = -1 ; G,C = 0 — matches genomic_trinary.GENETIC_MAP
-/

import FSOT.Formal.Genomic

namespace FSOT.Formal

noncomputable section

open Real

"""
    body: list[str] = [
        "def codon_table_count : ℕ := 64",
        f"def distinct_primary_codon_patterns : ℕ := {distinct_p}",
        f"def distinct_secondary_codon_patterns : ℕ := {distinct_s}",
        f"def stop_codon_count_cert : ℕ := {stop_count}",
        "",
        "theorem codon_table_count_eq_sixty_four :",
        "    codon_table_count = 64 := by",
        "  unfold codon_table_count; norm_num",
        "",
        "theorem codon_primary_pattern_space_eq_eight :",
        "    (2 : ℝ) ^ 3 = 8 := by norm_num",
        "",
        "theorem codon_secondary_pattern_space_eq_twenty_seven :",
        "    genetic_trinary_alphabet_card ^ 3 = 27 :=",
        "  codon_genetic_pattern_space_eq_twenty_seven",
        "",
        "theorem codon_genomic_table_link :",
        "    (4 : ℝ) ^ 3 = 64 := by",
        "  exact_mod_cast codon_table_size_eq_sixty_four",
        "",
        "theorem stop_codon_fraction_cert :",
        "    (3 : ℝ) / 64 = 0.046875 := by",
        "  exact stop_codons_fraction_eq",
        "",
    ]

    for row in rows:
        body.extend(emit_codon_block(row))

    anchor_primary_props = []
    anchor_secondary_props = []
    anchor_primary_proofs = []
    anchor_secondary_proofs = []
    for codon in ANCHOR_CODONS:
        row = row_by_codon[codon]
        name = codon.lower()
        p, s = row["primary"], row["secondary"]
        anchor_primary_props.append(
            f"(codon_{name}_primary_0, codon_{name}_primary_1, codon_{name}_primary_2) = ({p[0]}, {p[1]}, {p[2]})"
        )
        anchor_secondary_props.append(
            f"(codon_{name}_secondary_0, codon_{name}_secondary_1, codon_{name}_secondary_2) = ({s[0]}, {s[1]}, {s[2]})"
        )
        anchor_primary_proofs.append(f"codon_{name}_primary_phase")
        anchor_secondary_proofs.append(f"codon_{name}_secondary_phase")

    bundle_props = [
        "codon_table_count = 64",
        f"distinct_primary_codon_patterns = {distinct_p}",
        f"distinct_secondary_codon_patterns = {distinct_s}",
        f"stop_codon_count_cert = {stop_count}",
        "distinct_primary_codon_patterns ≤ 2 ^ 3",
        "distinct_secondary_codon_patterns ≤ genetic_trinary_alphabet_card ^ 3",
        "genetic_trinary_alphabet_card ^ 3 = 27",
        "(4 : ℝ) ^ 3 = 64",
        "(3 : ℝ) / 64 = 0.046875",
        *anchor_primary_props,
        *anchor_secondary_props,
    ]
    proofs = [
        "by unfold codon_table_count; norm_num",
        "by unfold distinct_primary_codon_patterns; norm_num",
        "by unfold distinct_secondary_codon_patterns; norm_num",
        "by unfold stop_codon_count_cert; norm_num",
        "by unfold distinct_primary_codon_patterns; norm_num",
        "by unfold distinct_secondary_codon_patterns genetic_trinary_alphabet_card; norm_num",
        "codon_secondary_pattern_space_eq_twenty_seven",
        "codon_genomic_table_link",
        "stop_codon_fraction_cert",
        *anchor_primary_proofs,
        *anchor_secondary_proofs,
    ]

    body.append("/-- Bundle: 64 codons, dual-axis trinary map linked to Genomic exact identities. -/")
    body.append("theorem codon_trinary_map_bundle :")
    for i, prop in enumerate(bundle_props):
        conj = " ∧" if i < len(bundle_props) - 1 else " := by"
        body.append(f"    {prop}{conj}")
    body.append(f"  refine ⟨{proofs[0]}, {proofs[1]}, {proofs[2]}, {proofs[3]}, {proofs[4]},")
    body.append(f"    {proofs[5]}, {proofs[6]}, {proofs[7]}, {proofs[8]},")
    for proof in proofs[9:]:
        suffix = "," if proof != proofs[-1] else "⟩"
        body.append(f"    {proof}{suffix}")
    body.extend(["", "end", "", "end FSOT.Formal", ""])
    return header + "\n".join(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CodonPriors.lean from lab registry")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    if not args.registry.exists():
        print(f"FAIL: missing {args.registry}")
        return 1

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    lean_src = build_lean(registry)
    args.output.write_text(lean_src, encoding="utf-8")
    print(f"Wrote {args.output} ({registry['codon_trinary_map']['codon_count']} codons)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())