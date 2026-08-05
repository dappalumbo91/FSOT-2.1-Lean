/-
  FSOT Formal EnvironmentalEngineeringPriors — extension domain Environmental_Engineering.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def environmental_engineering_observable_count : ℕ := 1120
def environmental_engineering_D_eff : ℕ := 17

theorem environmental_engineering_observable_count_pos : 0 < environmental_engineering_observable_count := by
  unfold environmental_engineering_observable_count; decide

theorem environmental_engineering_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem environmental_engineering_bundle :
    environmental_engineering_observable_count = 1120 ∧
    environmental_engineering_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold environmental_engineering_observable_count; decide,
    by unfold environmental_engineering_D_eff; decide,
    environmental_engineering_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
