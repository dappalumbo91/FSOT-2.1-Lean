/-
  FSOT Formal StumpedObservablesPanelPriors — Stumped_Observables_Panel Tier 51 stumped observables spine.
  Generator: scripts/gen_stumped_observables_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def stumped_panel_observable_count : ℕ := 13
def stumped_panel_pooled_median_error_pct : ℝ := (0.042611 : ℝ)
def stumped_panel_headline_median_error_pct : ℝ := (0.042611 : ℝ)
def stumped_panel_beats_sota_headlines : ℕ := 2
def stumped_panel_D_eff : ℕ := 22
def stumped_panel_open_prediction_count : ℕ := 5

theorem stumped_panel_observable_count_pos : 0 < stumped_panel_observable_count := by
  unfold stumped_panel_observable_count; norm_num

theorem stumped_panel_pooled_median_under_half_pct :
    stumped_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold stumped_panel_pooled_median_error_pct; norm_num

theorem stumped_panel_headline_median_under_half_pct :
    stumped_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold stumped_panel_headline_median_error_pct; norm_num

theorem stumped_panel_beats_sota_headlines_pos : 0 < stumped_panel_beats_sota_headlines := by
  unfold stumped_panel_beats_sota_headlines; norm_num
theorem stumped_panel_open_predictions_pos : 0 < stumped_panel_open_prediction_count := by unfold stumped_panel_open_prediction_count; norm_num

theorem stumped_panel_bundle :
    stumped_panel_observable_count = 13 ∧
    stumped_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    stumped_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold stumped_panel_observable_count; norm_num
  · exact stumped_panel_pooled_median_under_half_pct
  · exact stumped_panel_beats_sota_headlines_pos

end
