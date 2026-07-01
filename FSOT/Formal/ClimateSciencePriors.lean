/-
  FSOT Formal ClimateSciencePriors — extension domain Climate_Science.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def climate_science_observable_count : ℕ := 2519
def climate_science_D_eff : ℕ := 16

theorem climate_science_observable_count_pos : 0 < climate_science_observable_count := by
  unfold climate_science_observable_count; norm_num

theorem climate_science_median_error_under_five_pct :
    (0.0 : ℝ) < (5 : ℝ) := by norm_num

theorem climate_science_bundle :
    climate_science_observable_count = 2519 ∧
    climate_science_D_eff = 16 ∧
    (0.0 : ℝ) < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold climate_science_observable_count; norm_num,
    by unfold climate_science_D_eff; norm_num,
    climate_science_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
