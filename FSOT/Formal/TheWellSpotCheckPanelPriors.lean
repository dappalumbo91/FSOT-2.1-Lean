/-
  FSOT Formal TheWellSpotCheckPanelPriors — Tier 89 The Well verification (The_Well_Spot_Check_Panel).
  Generator: scripts/gen_tier89_the_well_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def the_well_spot_check_observable_count : ℕ := 12
def the_well_spot_check_median_error_pct : ℝ := (0.031159 : ℝ)
def the_well_spot_check_D_eff : ℕ := 18

theorem the_well_spot_check_observable_count_pos : 0 < the_well_spot_check_observable_count := by
  unfold the_well_spot_check_observable_count; norm_num

theorem the_well_spot_check_median_error_under_five_pct :
    the_well_spot_check_median_error_pct < (5 : ℝ) := by
  unfold the_well_spot_check_median_error_pct; norm_num

theorem the_well_spot_check_bundle :
    the_well_spot_check_observable_count = 12 ∧
    the_well_spot_check_D_eff = 18 ∧
    the_well_spot_check_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold the_well_spot_check_observable_count; norm_num,
    by unfold the_well_spot_check_D_eff; norm_num,
    the_well_spot_check_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
