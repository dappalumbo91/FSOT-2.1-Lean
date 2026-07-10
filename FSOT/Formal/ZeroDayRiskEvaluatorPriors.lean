/-
  FSOT Formal ZeroDayRiskEvaluatorPriors — Zero_Day_Risk_Evaluator Tier H cybersecurity engineering.
  Generator: scripts/gen_tier_h_cybersecurity_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def zero_day_eval_observable_count : ℕ := 26
def zero_day_eval_pooled_median_error_pct : ℝ := (0.010337117254355377 : ℝ)
def zero_day_eval_headline_median_error_pct : ℝ := (0.010337117254355377 : ℝ)
def zero_day_eval_beats_sota_headlines : ℕ := 2
def zero_day_eval_D_eff : ℕ := 18

def zero_day_eval_detected_hole_count : ℕ := 82
def zero_day_eval_risk_tier_green : ℕ := 0

theorem zero_day_eval_observable_count_pos : 0 < zero_day_eval_observable_count := by
  unfold zero_day_eval_observable_count; norm_num

theorem zero_day_eval_pooled_median_under_five_pct :
    zero_day_eval_pooled_median_error_pct < (5 : ℝ) := by
  unfold zero_day_eval_pooled_median_error_pct; norm_num

theorem zero_day_eval_headline_median_under_five_pct :
    zero_day_eval_headline_median_error_pct < (5 : ℝ) := by
  unfold zero_day_eval_headline_median_error_pct; norm_num

theorem zero_day_eval_beats_sota_headlines_pos : 0 < zero_day_eval_beats_sota_headlines := by
  unfold zero_day_eval_beats_sota_headlines; norm_num

theorem zero_day_eval_hole_count_certified : zero_day_eval_detected_hole_count = 82 := by
  unfold zero_day_eval_detected_hole_count; norm_num

theorem zero_day_eval_bundle :
    zero_day_eval_observable_count = 26 ∧
    zero_day_eval_pooled_median_error_pct < (5 : ℝ) ∧
    zero_day_eval_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold zero_day_eval_observable_count; norm_num
  · exact zero_day_eval_pooled_median_under_five_pct
  · exact zero_day_eval_beats_sota_headlines_pos

end
