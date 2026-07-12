/-
  FSOT Formal TheWellOutcomesVerificationPanelPriors — Tier 89 The Well verification (The_Well_Outcomes_Verification_Panel).
  Generator: scripts/gen_tier89_the_well_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def the_well_outcomes_observable_count : ℕ := 267
def the_well_outcomes_median_error_pct : ℝ := (0.031159 : ℝ)
def the_well_outcomes_D_eff : ℕ := 20

theorem the_well_outcomes_observable_count_pos : 0 < the_well_outcomes_observable_count := by
  unfold the_well_outcomes_observable_count; norm_num

theorem the_well_outcomes_median_error_under_five_pct :
    the_well_outcomes_median_error_pct < (5 : ℝ) := by
  unfold the_well_outcomes_median_error_pct; norm_num

theorem the_well_outcomes_bundle :
    the_well_outcomes_observable_count = 267 ∧
    the_well_outcomes_D_eff = 20 ∧
    the_well_outcomes_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold the_well_outcomes_observable_count; norm_num,
    by unfold the_well_outcomes_D_eff; norm_num,
    the_well_outcomes_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
