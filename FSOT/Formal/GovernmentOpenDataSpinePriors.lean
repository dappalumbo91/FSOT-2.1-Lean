/-
  FSOT Formal GovernmentOpenDataSpinePriors — Tier 80 government open data (Government_Open_Data_Spine).
  Generator: scripts/gen_tier80_government_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def government_open_data_spine_observable_count : ℕ := 28
def government_open_data_spine_median_error_pct : ℝ := (0.0 : ℝ)
def government_open_data_spine_D_eff : ℕ := 18

theorem government_open_data_spine_observable_count_pos : 0 < government_open_data_spine_observable_count := by
  unfold government_open_data_spine_observable_count; norm_num

theorem government_open_data_spine_median_error_under_five_pct :
    government_open_data_spine_median_error_pct < (5 : ℝ) := by
  unfold government_open_data_spine_median_error_pct; norm_num

theorem government_open_data_spine_bundle :
    government_open_data_spine_observable_count = 28 ∧
    government_open_data_spine_D_eff = 18 ∧
    government_open_data_spine_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold government_open_data_spine_observable_count; norm_num,
    by unfold government_open_data_spine_D_eff; norm_num,
    government_open_data_spine_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
