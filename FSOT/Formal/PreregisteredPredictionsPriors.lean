/-
  FSOT Formal PreregisteredPredictionsPriors — Preregistered_Predictions Tier K gap closure.
  Generator: scripts/gen_tier_k_toe_gap_closure_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def prereg_observable_count : ℕ := 8
def prereg_pooled_median_error_pct : ℝ := (0.02009823784840936 : ℝ)
def prereg_headline_median_error_pct : ℝ := (0.02009823784840936 : ℝ)
def prereg_beats_sota_headlines : ℕ := 2
def prereg_D_eff : ℕ := 17
def prereg_prediction_count : ℕ := 8
def prereg_discriminant_pass_count : ℕ := 8

theorem prereg_observable_count_pos : 0 < prereg_observable_count := by
  unfold prereg_observable_count; norm_num

theorem prereg_pooled_median_under_half_pct :
    prereg_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold prereg_pooled_median_error_pct; norm_num

theorem prereg_headline_median_under_half_pct :
    prereg_headline_median_error_pct < (0.5 : ℝ) := by
  unfold prereg_headline_median_error_pct; norm_num

theorem prereg_beats_sota_headlines_pos : 0 < prereg_beats_sota_headlines := by
  unfold prereg_beats_sota_headlines; norm_num
theorem prereg_predictions_pos : 0 < prereg_prediction_count := by unfold prereg_prediction_count; norm_num

theorem prereg_bundle :
    prereg_observable_count = 8 ∧
    prereg_pooled_median_error_pct < (0.5 : ℝ) ∧
    prereg_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold prereg_observable_count; norm_num
  · exact prereg_pooled_median_under_half_pct
  · exact prereg_beats_sota_headlines_pos

end
