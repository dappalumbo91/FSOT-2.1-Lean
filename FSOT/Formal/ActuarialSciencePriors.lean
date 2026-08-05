/-
  FSOT Formal ActuarialSciencePriors — Tier 82 scientific expansion (Actuarial_Science_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def actuarial_science_observable_count : ℕ := 60
def actuarial_science_median_error_pct : ℝ := (0.02261 : ℝ)
def actuarial_science_D_eff : ℕ := 20

theorem actuarial_science_observable_count_pos : 0 < actuarial_science_observable_count := by
  unfold actuarial_science_observable_count; decide

theorem actuarial_science_median_error_under_five_pct :
    actuarial_science_median_error_pct < (5 : ℝ) := by
  unfold actuarial_science_median_error_pct
  exact (by norm_num : (0.02261  : ℝ) < (5 : ℝ))

theorem actuarial_science_bundle :
    actuarial_science_observable_count = 60 ∧
    actuarial_science_D_eff = 20 ∧
    actuarial_science_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "economic") > 0 := by
  refine ⟨
    by unfold actuarial_science_observable_count; decide,
    by unfold actuarial_science_D_eff; decide,
    actuarial_science_median_error_under_five_pct,
    economic_raw_S_positive
  ⟩

end

end FSOT.Formal
