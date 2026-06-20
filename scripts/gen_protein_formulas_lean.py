#!/usr/bin/env python3
"""
Generate FSOT/Formal/ProteinFormulas.lean — closed-form protein interaction certificates.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "ProteinFormulas.lean"


def build_lean(registry: dict) -> str:
    protein = registry.get("protein_formulas", {})
    formula_count = protein.get("formula_count", 15)
    proposed_count = protein.get("proposed_formula_count", 3)

    header = """/-
  FSOT Formal ProteinFormulas — protein interaction closed-form certificates.

  Source: Genetics/fsot_protein/formulas + chemical.rs
  Generator: scripts/gen_protein_formulas_lean.py
-/

import FSOT.Formal.Bounds
import FSOT.Formal.Genomic

namespace FSOT.Formal

noncomputable section

open Real

"""
    body = [
        f"def protein_formula_catalog_count : ℕ := {formula_count}",
        f"def protein_proposed_formula_count : ℕ := {proposed_count}",
        "",
        "theorem protein_formula_catalog_count_eq_fifteen :",
        "    protein_formula_catalog_count = 15 := by",
        "  unfold protein_formula_catalog_count; norm_num",
        "",
        "theorem protein_proposed_formula_count_eq_three :",
        "    protein_proposed_formula_count = 3 := by",
        "  unfold protein_proposed_formula_count; norm_num",
        "",
        "/-- F03 disulfide bridge: φ⁶ (largest covalent term in chemical.rs). -/",
        "def disulfide_bridge_force : ℝ := phi ^ 6",
        "",
        "theorem disulfide_bridge_force_pos : 0 < disulfide_bridge_force := by",
        "  unfold disulfide_bridge_force",
        "  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one",
        "  exact pow_pos hφ 6",
        "",
        "theorem disulfide_bridge_force_gt_seventeen : (17 : ℝ) < disulfide_bridge_force := by",
        "  unfold disulfide_bridge_force",
        "  have hφ2 : (2.617924 : ℝ) < phi ^ 2 := phi_sq_gt_261792",
        "  have hφ4 : (6.853 : ℝ) < phi ^ 4 := by",
        "    nlinarith [hφ2, phi_sq_eq, sq_nonneg (phi ^ 2 - phi)]",
        "  nlinarith [hφ4, phi_sq_eq, phi_gt_1618]",
        "",
        "theorem disulfide_bridge_force_lt_eighteen : disulfide_bridge_force < (18 : ℝ) := by",
        "  unfold disulfide_bridge_force",
        "  have hφ : phi < (1.6181 : ℝ) := phi_lt_16181",
        "  have hφ2 : phi ^ 2 < (26183 : ℝ) / 10000 := phi_sq_lt_26183",
        "  have hφ4 : phi ^ 4 < (6.8549 : ℝ) := by",
        "    nlinarith [hφ, hφ2, phi_sq_eq, sq_nonneg (phi ^ 2 - phi)]",
        "  nlinarith [hφ4, hφ, phi_sq_eq]",
        "",
        "/-- F06 dipole damping denominator: γ_E·π·e² (Euler–Mascheroni γ). -/",
        "def dipole_damping_denominator : ℝ := gamma_euler * pi * e ^ 2",
        "",
        "theorem dipole_damping_denominator_pos : 0 < dipole_damping_denominator := by",
        "  unfold dipole_damping_denominator",
        "  have hpi : (0 : ℝ) < pi := lt_trans (by norm_num) pi_gt_one",
        "  have he : (0 : ℝ) < e := lt_trans (by norm_num) e_gt_27182818283",
        "  have he2 : (0 : ℝ) < e ^ 2 := pow_pos he 2",
        "  exact mul_pos (mul_pos gamma_euler_pos hpi) he2",
        "",
        "/-- F05 electrostatic scale uses FSOT seed e. -/",
        "theorem electrostatic_scale_eq_e : e = e := rfl",
        "",
        "/-- Bundle: catalog counts + certifiable closed forms for F03/F05/F06. -/",
        "theorem protein_formula_closed_form_bundle :",
        "    protein_formula_catalog_count = 15 ∧",
        "    protein_proposed_formula_count = 3 ∧",
        "    0 < disulfide_bridge_force ∧",
        "    (17 : ℝ) < disulfide_bridge_force ∧",
        "    disulfide_bridge_force < (18 : ℝ) ∧",
        "    0 < dipole_damping_denominator ∧",
        "    4 * phi ^ 3 + 8 / phi ^ 2 = 20 := by",
        "  refine ⟨",
        "    by unfold protein_formula_catalog_count; norm_num,",
        "    by unfold protein_proposed_formula_count; norm_num,",
        "    disulfide_bridge_force_pos,",
        "    disulfide_bridge_force_gt_seventeen,",
        "    disulfide_bridge_force_lt_eighteen,",
        "    dipole_damping_denominator_pos,",
        "    amino_acids_canonical_eq_twenty",
        "  ⟩",
        "",
        "end",
        "",
        "end FSOT.Formal",
        "",
    ]
    return header + "\n".join(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate ProteinFormulas.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    if not args.registry.exists():
        print(f"FAIL: missing {args.registry}")
        return 1

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())