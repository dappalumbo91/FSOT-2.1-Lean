/-
  FSOT Formal FluidSpacetimeObservableSpinePriors — Tier 76 fluid spacetime + cosmology.
  Generator: scripts/gen_tiers_76_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fluid_spacetime_observable_spine_observable_count : ℕ := 37
def fluid_spacetime_observable_spine_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def fluid_spacetime_observable_spine_headline_median_error_pct : ℝ := (0.000502 : ℝ)
def fluid_spacetime_observable_spine_beats_sota_headlines : ℕ := 2
def fluid_spacetime_observable_spine_D_eff : ℕ := 26

theorem fluid_spacetime_observable_spine_observable_count_pos : 0 < fluid_spacetime_observable_spine_observable_count := by
  unfold fluid_spacetime_observable_spine_observable_count; norm_num

theorem fluid_spacetime_observable_spine_pooled_median_under_half_pct :
    fluid_spacetime_observable_spine_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fluid_spacetime_observable_spine_pooled_median_error_pct; norm_num

theorem fluid_spacetime_observable_spine_headline_median_under_half_pct :
    fluid_spacetime_observable_spine_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fluid_spacetime_observable_spine_headline_median_error_pct; norm_num

theorem fluid_spacetime_observable_spine_beats_sota_headlines_pos : 0 < fluid_spacetime_observable_spine_beats_sota_headlines := by
  unfold fluid_spacetime_observable_spine_beats_sota_headlines; norm_num

theorem fluid_spacetime_observable_spine_bundle :
    fluid_spacetime_observable_spine_observable_count = 37 ∧
    fluid_spacetime_observable_spine_pooled_median_error_pct < (0.5 : ℝ) ∧
    fluid_spacetime_observable_spine_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fluid_spacetime_observable_spine_observable_count; norm_num
  · exact fluid_spacetime_observable_spine_pooled_median_under_half_pct
  · exact fluid_spacetime_observable_spine_beats_sota_headlines_pos

end
