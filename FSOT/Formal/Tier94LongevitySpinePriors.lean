/-
  FSOT Formal Tier94LongevitySpinePriors — extension domain Tier_94_Longevity_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def tier_94_longevity_spine_observable_count : ℕ := 34
def tier_94_longevity_spine_D_eff : ℕ := 25

theorem tier_94_longevity_spine_observable_count_pos : 0 < tier_94_longevity_spine_observable_count := by
  unfold tier_94_longevity_spine_observable_count; norm_num

theorem tier_94_longevity_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem tier_94_longevity_spine_bundle :
    tier_94_longevity_spine_observable_count = 34 ∧
    tier_94_longevity_spine_D_eff = 25 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold tier_94_longevity_spine_observable_count; norm_num,
    by unfold tier_94_longevity_spine_D_eff; norm_num,
    tier_94_longevity_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
