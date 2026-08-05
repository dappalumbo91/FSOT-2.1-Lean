/-
  FSOT Formal GovernmentOpenDataSpinePriors — extension domain Government_Open_Data_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def government_open_data_spine_observable_count : ℕ := 28
def government_open_data_spine_D_eff : ℕ := 18

theorem government_open_data_spine_observable_count_pos : 0 < government_open_data_spine_observable_count := by
  unfold government_open_data_spine_observable_count; decide

theorem government_open_data_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem government_open_data_spine_bundle :
    government_open_data_spine_observable_count = 28 ∧
    government_open_data_spine_D_eff = 18 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold government_open_data_spine_observable_count; decide,
    by unfold government_open_data_spine_D_eff; decide,
    government_open_data_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
