/-
  FSOT Formal FsotAggregateOrganizedPanelPriors — Tier 68–70 expansion.
  Generator: scripts/gen_tiers_68_70_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_aggregate_organized_panel_observable_count : ℕ := 10
def fsot_aggregate_organized_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_aggregate_organized_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_aggregate_organized_panel_beats_sota_headlines : ℕ := 2
def fsot_aggregate_organized_panel_D_eff : ℕ := 17

theorem fsot_aggregate_organized_panel_observable_count_pos : 0 < fsot_aggregate_organized_panel_observable_count := by
  unfold fsot_aggregate_organized_panel_observable_count; norm_num

theorem fsot_aggregate_organized_panel_pooled_median_under_half_pct :
    fsot_aggregate_organized_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_aggregate_organized_panel_pooled_median_error_pct; norm_num

theorem fsot_aggregate_organized_panel_headline_median_under_half_pct :
    fsot_aggregate_organized_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_aggregate_organized_panel_headline_median_error_pct; norm_num

theorem fsot_aggregate_organized_panel_beats_sota_headlines_pos : 0 < fsot_aggregate_organized_panel_beats_sota_headlines := by
  unfold fsot_aggregate_organized_panel_beats_sota_headlines; norm_num

theorem fsot_aggregate_organized_panel_bundle :
    fsot_aggregate_organized_panel_observable_count = 10 ∧
    fsot_aggregate_organized_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    fsot_aggregate_organized_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fsot_aggregate_organized_panel_observable_count; norm_num
  · exact fsot_aggregate_organized_panel_pooled_median_under_half_pct
  · exact fsot_aggregate_organized_panel_beats_sota_headlines_pos

end
