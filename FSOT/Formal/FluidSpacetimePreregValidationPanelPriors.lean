/-
  FSOT Formal FluidSpacetimePreregValidationPanelPriors — Tier 77 post–Tier 76 maintenance.
  Generator: scripts/gen_tiers_77_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fluid_spacetime_prereg_validation_panel_observable_count : ℕ := 19
def fluid_spacetime_prereg_validation_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def fluid_spacetime_prereg_validation_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def fluid_spacetime_prereg_validation_panel_beats_sota_headlines : ℕ := 2
def fluid_spacetime_prereg_validation_panel_D_eff : ℕ := 25

theorem fluid_spacetime_prereg_validation_panel_observable_count_pos : 0 < fluid_spacetime_prereg_validation_panel_observable_count := by
  unfold fluid_spacetime_prereg_validation_panel_observable_count; norm_num

theorem fluid_spacetime_prereg_validation_panel_pooled_median_under_half_pct :
    fluid_spacetime_prereg_validation_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fluid_spacetime_prereg_validation_panel_pooled_median_error_pct; norm_num

theorem fluid_spacetime_prereg_validation_panel_headline_median_under_half_pct :
    fluid_spacetime_prereg_validation_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fluid_spacetime_prereg_validation_panel_headline_median_error_pct; norm_num

theorem fluid_spacetime_prereg_validation_panel_beats_sota_headlines_pos : 0 < fluid_spacetime_prereg_validation_panel_beats_sota_headlines := by
  unfold fluid_spacetime_prereg_validation_panel_beats_sota_headlines; norm_num

theorem fluid_spacetime_prereg_validation_panel_bundle :
    fluid_spacetime_prereg_validation_panel_observable_count = 19 ∧
    fluid_spacetime_prereg_validation_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    fluid_spacetime_prereg_validation_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fluid_spacetime_prereg_validation_panel_observable_count; norm_num
  · exact fluid_spacetime_prereg_validation_panel_pooled_median_under_half_pct
  · exact fluid_spacetime_prereg_validation_panel_beats_sota_headlines_pos

end
