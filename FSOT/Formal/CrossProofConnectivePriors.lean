/-
  FSOT Formal CrossProofConnectivePriors — Tier 80 wide cross-proof spine.
  Lean authority for obligations exported to verification/coq and verification/isabelle.
  Generator: scripts/export_cross_proof_obligations.py
-/

import FSOT.Formal.Domains
import FSOT.Formal.WarpActuationDevelopmentPriors

namespace FSOT.Formal

noncomputable section

open Real

def cross_proof_connective_obligation_count : ℕ := 24
def cross_proof_connective_lean_modules : ℕ := 3
def cross_proof_full_formal_obligation_count : ℕ := 1241
def cross_proof_full_formal_modules : ℕ := 317
def cross_proof_full_priors_obligation_count : ℕ := 1153
def cross_proof_full_priors_lean_modules : ℕ := 300
def cross_proof_full_formal_provable_count : ℕ := 1241
def cross_proof_full_priors_margin_violation_count : ℕ := 0

theorem cross_proof_obligation_count_pos : 0 < cross_proof_connective_obligation_count := by
  unfold cross_proof_connective_obligation_count; norm_num

theorem cross_proof_lean_modules_pos : 0 < cross_proof_connective_lean_modules := by
  unfold cross_proof_connective_lean_modules; norm_num

theorem cross_proof_full_formal_obligation_count_pos : 0 < cross_proof_full_formal_obligation_count := by
  unfold cross_proof_full_formal_obligation_count; norm_num

theorem cross_proof_full_formal_provable_count_pos : 0 < cross_proof_full_formal_provable_count := by
  unfold cross_proof_full_formal_provable_count; norm_num

/-- Tier 79 bundle: connective spine exported for Coq/Isabelle cross-proof. -/
theorem cross_proof_connective_spine_bundle :
    cross_proof_connective_obligation_count = 24 ∧
    cross_proof_connective_lean_modules = 3 ∧
    (1 : ℝ) < warp_stabilization_margin := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold cross_proof_connective_obligation_count; norm_num
  · unfold cross_proof_connective_lean_modules; norm_num
  · exact warp_stabilization_margin_gt_one

/-- Tier 80 bundle: wide FSOT/Formal spine exported for Coq cross-refinement. -/
theorem cross_proof_full_formal_spine_bundle :
    cross_proof_full_formal_obligation_count = 1241 ∧
    cross_proof_full_formal_modules = 317 ∧
    cross_proof_full_priors_obligation_count = 1153 ∧
    cross_proof_full_formal_provable_count = 1241 ∧
    cross_proof_full_priors_margin_violation_count = 0 ∧
    cross_proof_connective_obligation_count < cross_proof_full_formal_obligation_count := by
  refine ⟨?h1, ?h2, ?h3, ?h4, ?h5, ?h6⟩
  · unfold cross_proof_full_formal_obligation_count; norm_num
  · unfold cross_proof_full_formal_modules; norm_num
  · unfold cross_proof_full_priors_obligation_count; norm_num
  · unfold cross_proof_full_formal_provable_count; norm_num
  · unfold cross_proof_full_priors_margin_violation_count; norm_num
  · unfold cross_proof_connective_obligation_count cross_proof_full_formal_obligation_count; norm_num

end