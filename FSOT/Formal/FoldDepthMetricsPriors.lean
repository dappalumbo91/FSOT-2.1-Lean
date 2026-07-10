/-
  FSOT Formal FoldDepthMetricsPriors — Fold_Depth_Metrics Tier N compactification ladder.
  Generator: scripts/gen_tier_n_compactification_ladder_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fold_dep_observable_count : ℕ := 51
def fold_dep_pooled_median_error_pct : ℝ := (0.025753835305195434 : ℝ)
def fold_dep_headline_median_error_pct : ℝ := (0.025753835305195434 : ℝ)
def fold_dep_beats_sota_headlines : ℕ := 2
def fold_dep_D_eff : ℕ := 20
def fold_dep_fold_span_ten_thousandths : ℕ := 27193

theorem fold_dep_observable_count_pos : 0 < fold_dep_observable_count := by
  unfold fold_dep_observable_count; norm_num

theorem fold_dep_pooled_median_under_five_pct :
    fold_dep_pooled_median_error_pct < (5 : ℝ) := by
  unfold fold_dep_pooled_median_error_pct; norm_num

theorem fold_dep_headline_median_under_five_pct :
    fold_dep_headline_median_error_pct < (5 : ℝ) := by
  unfold fold_dep_headline_median_error_pct; norm_num

theorem fold_dep_beats_sota_headlines_pos : 0 < fold_dep_beats_sota_headlines := by
  unfold fold_dep_beats_sota_headlines; norm_num
theorem fold_dep_fold_span_pos : 0 < fold_dep_fold_span_ten_thousandths := by unfold fold_dep_fold_span_ten_thousandths; norm_num

theorem fold_dep_bundle :
    fold_dep_observable_count = 51 ∧
    fold_dep_pooled_median_error_pct < (5 : ℝ) ∧
    fold_dep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fold_dep_observable_count; norm_num
  · exact fold_dep_pooled_median_under_five_pct
  · exact fold_dep_beats_sota_headlines_pos

end
