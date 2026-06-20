/-
  FSOT Formal LeanProofsBridge — FSOT_Lean_Proofs formal constant bridge certificates.

  Source: FSOT_Lean_Proofs/FSOT_Formal_Output.json
  Generator: scripts/gen_lean_proofs_bridge_lean.py
-/

import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

open Real

def lean_proofs_formal_constant_count : ℕ := 28
def lean_proofs_domain_proven_count : ℕ := 28

theorem lean_proofs_formal_constant_count_pos : 0 < lean_proofs_formal_constant_count := by
  unfold lean_proofs_formal_constant_count; norm_num

theorem lean_proofs_domain_proven_count_pos : 0 < lean_proofs_domain_proven_count := by
  unfold lean_proofs_domain_proven_count; norm_num

theorem lean_proofs_domain_proven_le_formal :
    lean_proofs_domain_proven_count ≤ lean_proofs_formal_constant_count := by
  unfold lean_proofs_domain_proven_count lean_proofs_formal_constant_count; norm_num

/-- Bundle: formalized constants with SMILES k-alignment certificate. -/
theorem lean_proofs_constant_bundle :
    lean_proofs_formal_constant_count = 28 ∧
    lean_proofs_domain_proven_count = 28 ∧
    lean_proofs_domain_proven_count ≤ lean_proofs_formal_constant_count ∧
    |k - smiles_k_cached| < (5e-4 : ℝ) := by
  refine ⟨
    by unfold lean_proofs_formal_constant_count; norm_num,
    by unfold lean_proofs_domain_proven_count; norm_num,
    lean_proofs_domain_proven_le_formal,
    smiles_k_matches_formal_k
  ⟩

end

end FSOT.Formal
