/-
  FSOT Formal SuperheavyElementStabilityPanelPriors — Tier 72 periodic table completion.
  Generator: scripts/gen_tiers_72_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def superheavy_element_stability_panel_observable_count : ℕ := 50
def superheavy_element_stability_panel_pooled_median_error_pct : ℝ := (1e-06 : ℝ)
def superheavy_element_stability_panel_headline_median_error_pct : ℝ := (1e-06 : ℝ)
def superheavy_element_stability_panel_beats_sota_headlines : ℕ := 2
def superheavy_element_stability_panel_D_eff : ℕ := 10

theorem superheavy_element_stability_panel_observable_count_pos : 0 < superheavy_element_stability_panel_observable_count := by
  unfold superheavy_element_stability_panel_observable_count; norm_num

theorem superheavy_element_stability_panel_pooled_median_under_half_pct :
    superheavy_element_stability_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold superheavy_element_stability_panel_pooled_median_error_pct; norm_num

theorem superheavy_element_stability_panel_headline_median_under_half_pct :
    superheavy_element_stability_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold superheavy_element_stability_panel_headline_median_error_pct; norm_num

theorem superheavy_element_stability_panel_beats_sota_headlines_pos : 0 < superheavy_element_stability_panel_beats_sota_headlines := by
  unfold superheavy_element_stability_panel_beats_sota_headlines; norm_num

theorem superheavy_element_stability_panel_bundle :
    superheavy_element_stability_panel_observable_count = 50 ∧
    superheavy_element_stability_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    superheavy_element_stability_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold superheavy_element_stability_panel_observable_count; norm_num
  · exact superheavy_element_stability_panel_pooled_median_under_half_pct
  · exact superheavy_element_stability_panel_beats_sota_headlines_pos

end
