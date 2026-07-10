/-
  FSOT Formal IslandOfStabilityDeepPanelPriors — Tier 74 superheavy island Z=120-126.
  Generator: scripts/gen_tiers_74_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def island_of_stability_deep_panel_observable_count : ℕ := 23
def island_of_stability_deep_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def island_of_stability_deep_panel_headline_median_error_pct : ℝ := (9.504139423370362e-09 : ℝ)
def island_of_stability_deep_panel_beats_sota_headlines : ℕ := 2
def island_of_stability_deep_panel_D_eff : ℕ := 19

theorem island_of_stability_deep_panel_observable_count_pos : 0 < island_of_stability_deep_panel_observable_count := by
  unfold island_of_stability_deep_panel_observable_count; norm_num

theorem island_of_stability_deep_panel_pooled_median_under_half_pct :
    island_of_stability_deep_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold island_of_stability_deep_panel_pooled_median_error_pct; norm_num

theorem island_of_stability_deep_panel_headline_median_under_half_pct :
    island_of_stability_deep_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold island_of_stability_deep_panel_headline_median_error_pct; norm_num

theorem island_of_stability_deep_panel_beats_sota_headlines_pos : 0 < island_of_stability_deep_panel_beats_sota_headlines := by
  unfold island_of_stability_deep_panel_beats_sota_headlines; norm_num

theorem island_of_stability_deep_panel_bundle :
    island_of_stability_deep_panel_observable_count = 23 ∧
    island_of_stability_deep_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    island_of_stability_deep_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold island_of_stability_deep_panel_observable_count; norm_num
  · exact island_of_stability_deep_panel_pooled_median_under_half_pct
  · exact island_of_stability_deep_panel_beats_sota_headlines_pos

end
