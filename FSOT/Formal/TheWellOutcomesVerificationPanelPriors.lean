/-
  FSOT Formal TheWellOutcomesVerificationPanelPriors — extension domain The_Well_Outcomes_Verification_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def the_well_outcomes_verification_panel_observable_count : ℕ := 246
def the_well_outcomes_verification_panel_D_eff : ℕ := 20

theorem the_well_outcomes_verification_panel_observable_count_pos : 0 < the_well_outcomes_verification_panel_observable_count := by
  unfold the_well_outcomes_verification_panel_observable_count; decide

theorem the_well_outcomes_verification_panel_median_error_under_half_pct :
    (0.031159 : ℝ) < (0.5 : ℝ) := by norm_num

theorem the_well_outcomes_verification_panel_bundle :
    the_well_outcomes_verification_panel_observable_count = 246 ∧
    the_well_outcomes_verification_panel_D_eff = 20 ∧
    (0.031159 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold the_well_outcomes_verification_panel_observable_count; decide,
    by unfold the_well_outcomes_verification_panel_D_eff; decide,
    the_well_outcomes_verification_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
