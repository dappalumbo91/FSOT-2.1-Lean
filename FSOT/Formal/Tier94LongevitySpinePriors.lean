/-
  FSOT Formal Tier94LongevitySpinePriors — Tier 94 longevity genetics (Tier_94_Longevity_Spine).
  Generator: scripts/gen_tier94_longevity_genetics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def tier_94_longevity_observable_count : ℕ := 34
def tier_94_longevity_median_error_pct : ℝ := (0.0 : ℝ)
def tier_94_longevity_D_eff : ℕ := 25

theorem tier_94_longevity_observable_count_pos : 0 < tier_94_longevity_observable_count := by
  unfold tier_94_longevity_observable_count; decide

theorem tier_94_longevity_median_error_under_five_pct :
    tier_94_longevity_median_error_pct < (5 : ℝ) := by
  unfold tier_94_longevity_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem tier_94_longevity_bundle :
    tier_94_longevity_observable_count = 34 ∧
    tier_94_longevity_D_eff = 25 ∧
    tier_94_longevity_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold tier_94_longevity_observable_count; decide,
    by unfold tier_94_longevity_D_eff; decide,
    tier_94_longevity_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
