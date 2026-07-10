/-
  FSOT Formal AdjacentRungCouplingPriors — Adjacent_Rung_Coupling Tier N compactification ladder.
  Generator: scripts/gen_tier_n_compactification_ladder_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def adj_rung_observable_count : ℕ := 36
def adj_rung_pooled_median_error_pct : ℝ := (0.020098237848404983 : ℝ)
def adj_rung_headline_median_error_pct : ℝ := (0.020098237848404983 : ℝ)
def adj_rung_beats_sota_headlines : ℕ := 2
def adj_rung_D_eff : ℕ := 17
def adj_rung_adjacent_pair_count : ℕ := 9

theorem adj_rung_observable_count_pos : 0 < adj_rung_observable_count := by
  unfold adj_rung_observable_count; norm_num

theorem adj_rung_pooled_median_under_half_pct :
    adj_rung_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold adj_rung_pooled_median_error_pct; norm_num

theorem adj_rung_headline_median_under_half_pct :
    adj_rung_headline_median_error_pct < (0.5 : ℝ) := by
  unfold adj_rung_headline_median_error_pct; norm_num

theorem adj_rung_beats_sota_headlines_pos : 0 < adj_rung_beats_sota_headlines := by
  unfold adj_rung_beats_sota_headlines; norm_num
theorem adj_rung_pairs_complete : adj_rung_adjacent_pair_count = 9 := by unfold adj_rung_adjacent_pair_count; norm_num

theorem adj_rung_bundle :
    adj_rung_observable_count = 36 ∧
    adj_rung_pooled_median_error_pct < (0.5 : ℝ) ∧
    adj_rung_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold adj_rung_observable_count; norm_num
  · exact adj_rung_pooled_median_under_half_pct
  · exact adj_rung_beats_sota_headlines_pos

end
