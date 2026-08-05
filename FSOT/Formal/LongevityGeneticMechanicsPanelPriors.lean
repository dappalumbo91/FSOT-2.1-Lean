/-
  FSOT Formal LongevityGeneticMechanicsPanelPriors — Tier 94 longevity genetics (Longevity_Genetic_Mechanics_Panel).
  Generator: scripts/gen_tier94_longevity_genetics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def longevity_genetic_mechanics_observable_count : ℕ := 35
def longevity_genetic_mechanics_median_error_pct : ℝ := (0.022236 : ℝ)
def longevity_genetic_mechanics_D_eff : ℕ := 19

theorem longevity_genetic_mechanics_observable_count_pos : 0 < longevity_genetic_mechanics_observable_count := by
  unfold longevity_genetic_mechanics_observable_count; decide

theorem longevity_genetic_mechanics_median_error_under_five_pct :
    longevity_genetic_mechanics_median_error_pct < (5 : ℝ) := by
  unfold longevity_genetic_mechanics_median_error_pct
  exact (by norm_num : (0.022236  : ℝ) < (5 : ℝ))

theorem longevity_genetic_mechanics_bundle :
    longevity_genetic_mechanics_observable_count = 35 ∧
    longevity_genetic_mechanics_D_eff = 19 ∧
    longevity_genetic_mechanics_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold longevity_genetic_mechanics_observable_count; decide,
    by unfold longevity_genetic_mechanics_D_eff; decide,
    longevity_genetic_mechanics_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
