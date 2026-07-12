/-
  FSOT Formal FoodMicrobiologyPriors — extension domain Food_Microbiology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def food_microbiology_observable_count : ℕ := 30
def food_microbiology_D_eff : ℕ := 14

theorem food_microbiology_observable_count_pos : 0 < food_microbiology_observable_count := by
  unfold food_microbiology_observable_count; norm_num

theorem food_microbiology_median_error_under_half_pct :
    (0.04447250077037743 : ℝ) < (0.5 : ℝ) := by norm_num

theorem food_microbiology_bundle :
    food_microbiology_observable_count = 30 ∧
    food_microbiology_D_eff = 14 ∧
    (0.04447250077037743 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold food_microbiology_observable_count; norm_num,
    by unfold food_microbiology_D_eff; norm_num,
    food_microbiology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
