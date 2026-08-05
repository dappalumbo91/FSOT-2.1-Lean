/-
  FSOT Formal CodingStructureVerifierPanelPriors — engineering/code residual panel (Coding_Structure_Verifier_Panel).
  Generator: scripts/gen_engineering_code_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def coding_structure_verifier_observable_count : ℕ := 18
def coding_structure_verifier_median_error_pct : ℝ := (0.0 : ℝ)
def coding_structure_verifier_D_eff : ℕ := 14

theorem coding_structure_verifier_observable_count_pos : 0 < coding_structure_verifier_observable_count := by
  unfold coding_structure_verifier_observable_count; decide

theorem coding_structure_verifier_median_error_under_half_pct :
    coding_structure_verifier_median_error_pct < (0.5 : ℝ) := by
  unfold coding_structure_verifier_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem coding_structure_verifier_bundle :
    coding_structure_verifier_observable_count = 18 ∧
    coding_structure_verifier_D_eff = 14 ∧
    coding_structure_verifier_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold coding_structure_verifier_observable_count; decide,
    by unfold coding_structure_verifier_D_eff; decide,
    coding_structure_verifier_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
