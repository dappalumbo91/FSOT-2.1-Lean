/-
  FSOT Formal DomainOrbitalPredictionsPriors — Domain_Orbital_Predictions Tier L orbital gap fill.
  Generator: scripts/gen_tier_l_orbital_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def orb_pred_observable_count : ℕ := 17
def orb_pred_pooled_median_error_pct : ℝ := (0.03147898006445882 : ℝ)
def orb_pred_headline_median_error_pct : ℝ := (0.03147898006445882 : ℝ)
def orb_pred_beats_sota_headlines : ℕ := 2
def orb_pred_D_eff : ℕ := 18
def orb_pred_prediction_count : ℕ := 12
def orb_pred_filled_prediction_count : ℕ := 9

theorem orb_pred_observable_count_pos : 0 < orb_pred_observable_count := by
  unfold orb_pred_observable_count; norm_num

theorem orb_pred_pooled_median_under_five_pct :
    orb_pred_pooled_median_error_pct < (5 : ℝ) := by
  unfold orb_pred_pooled_median_error_pct; norm_num

theorem orb_pred_headline_median_under_five_pct :
    orb_pred_headline_median_error_pct < (5 : ℝ) := by
  unfold orb_pred_headline_median_error_pct; norm_num

theorem orb_pred_beats_sota_headlines_pos : 0 < orb_pred_beats_sota_headlines := by
  unfold orb_pred_beats_sota_headlines; norm_num
theorem orb_pred_filled_predictions_pos : 0 < orb_pred_filled_prediction_count := by unfold orb_pred_filled_prediction_count; norm_num

theorem orb_pred_bundle :
    orb_pred_observable_count = 17 ∧
    orb_pred_pooled_median_error_pct < (5 : ℝ) ∧
    orb_pred_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold orb_pred_observable_count; norm_num
  · exact orb_pred_pooled_median_under_five_pct
  · exact orb_pred_beats_sota_headlines_pos

end
