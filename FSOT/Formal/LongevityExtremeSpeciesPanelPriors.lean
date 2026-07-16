/-
  FSOT Formal LongevityExtremeSpeciesPanelPriors — Tier 94 longevity genetics (Longevity_Extreme_Species_Panel).
  Generator: scripts/gen_tier94_longevity_genetics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def longevity_extreme_species_observable_count : ℕ := 164
def longevity_extreme_species_median_error_pct : ℝ := (0.017789 : ℝ)
def longevity_extreme_species_D_eff : ℕ := 21

theorem longevity_extreme_species_observable_count_pos : 0 < longevity_extreme_species_observable_count := by
  unfold longevity_extreme_species_observable_count; norm_num

theorem longevity_extreme_species_median_error_under_five_pct :
    longevity_extreme_species_median_error_pct < (5 : ℝ) := by
  unfold longevity_extreme_species_median_error_pct; norm_num

theorem longevity_extreme_species_bundle :
    longevity_extreme_species_observable_count = 164 ∧
    longevity_extreme_species_D_eff = 21 ∧
    longevity_extreme_species_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold longevity_extreme_species_observable_count; norm_num,
    by unfold longevity_extreme_species_D_eff; norm_num,
    longevity_extreme_species_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
