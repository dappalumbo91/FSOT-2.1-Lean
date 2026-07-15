/-
  FSOT Formal EarlyLeanMcPanelPriors — Tier 88 application wiring (Early_Lean_MC_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def early_lean_mc_observable_count : ℕ := 10
def early_lean_mc_median_error_pct : ℝ := (0.014767 : ℝ)
def early_lean_mc_D_eff : ℕ := 11

theorem early_lean_mc_observable_count_pos : 0 < early_lean_mc_observable_count := by
  unfold early_lean_mc_observable_count; norm_num

theorem early_lean_mc_median_error_under_five_pct :
    early_lean_mc_median_error_pct < (5 : ℝ) := by
  unfold early_lean_mc_median_error_pct; norm_num

theorem early_lean_mc_bundle :
    early_lean_mc_observable_count = 10 ∧
    early_lean_mc_D_eff = 11 ∧
    early_lean_mc_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "mathematical") > 0 := by
  refine ⟨
    by unfold early_lean_mc_observable_count; norm_num,
    by unfold early_lean_mc_D_eff; norm_num,
    early_lean_mc_median_error_under_five_pct,
    mathematical_raw_S_positive
  ⟩

end

end FSOT.Formal
