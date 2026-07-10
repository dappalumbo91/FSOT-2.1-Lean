/-
  FSOT Formal TimeEmergenceDeepPanelPriors — Tier 76 fluid spacetime + cosmology.
  Generator: scripts/gen_tiers_76_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def time_emergence_deep_panel_observable_count : ℕ := 17
def time_emergence_deep_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def time_emergence_deep_panel_headline_median_error_pct : ℝ := (5.0245583893760355e-08 : ℝ)
def time_emergence_deep_panel_beats_sota_headlines : ℕ := 2
def time_emergence_deep_panel_D_eff : ℕ := 19

theorem time_emergence_deep_panel_observable_count_pos : 0 < time_emergence_deep_panel_observable_count := by
  unfold time_emergence_deep_panel_observable_count; norm_num

theorem time_emergence_deep_panel_pooled_median_under_half_pct :
    time_emergence_deep_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold time_emergence_deep_panel_pooled_median_error_pct; norm_num

theorem time_emergence_deep_panel_headline_median_under_half_pct :
    time_emergence_deep_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold time_emergence_deep_panel_headline_median_error_pct; norm_num

theorem time_emergence_deep_panel_beats_sota_headlines_pos : 0 < time_emergence_deep_panel_beats_sota_headlines := by
  unfold time_emergence_deep_panel_beats_sota_headlines; norm_num

theorem time_emergence_deep_panel_bundle :
    time_emergence_deep_panel_observable_count = 17 ∧
    time_emergence_deep_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    time_emergence_deep_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold time_emergence_deep_panel_observable_count; norm_num
  · exact time_emergence_deep_panel_pooled_median_under_half_pct
  · exact time_emergence_deep_panel_beats_sota_headlines_pos

end
