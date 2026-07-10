/-
  FSOT Formal RealityFoldingSpinePriors — Reality_Folding_Spine Tier N compactification ladder.
  Generator: scripts/gen_tier_n_compactification_ladder_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fold_spine_observable_count : ℕ := 8
def fold_spine_pooled_median_error_pct : ℝ := (0.019008268802505057 : ℝ)
def fold_spine_headline_median_error_pct : ℝ := (0.019008268802505057 : ℝ)
def fold_spine_beats_sota_headlines : ℕ := 2
def fold_spine_D_eff : ℕ := 21
def fold_spine_ladder_rung_count : ℕ := 10
def fold_spine_adjacent_pair_count : ℕ := 9
def fold_spine_coupling_node_count : ℕ := 179

theorem fold_spine_observable_count_pos : 0 < fold_spine_observable_count := by
  unfold fold_spine_observable_count; norm_num

theorem fold_spine_pooled_median_under_five_pct :
    fold_spine_pooled_median_error_pct < (5 : ℝ) := by
  unfold fold_spine_pooled_median_error_pct; norm_num

theorem fold_spine_headline_median_under_five_pct :
    fold_spine_headline_median_error_pct < (5 : ℝ) := by
  unfold fold_spine_headline_median_error_pct; norm_num

theorem fold_spine_beats_sota_headlines_pos : 0 < fold_spine_beats_sota_headlines := by
  unfold fold_spine_beats_sota_headlines; norm_num
theorem fold_spine_ladder_rungs_pos : 0 < fold_spine_ladder_rung_count := by unfold fold_spine_ladder_rung_count; norm_num

theorem fold_spine_bundle :
    fold_spine_observable_count = 8 ∧
    fold_spine_pooled_median_error_pct < (5 : ℝ) ∧
    fold_spine_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fold_spine_observable_count; norm_num
  · exact fold_spine_pooled_median_under_five_pct
  · exact fold_spine_beats_sota_headlines_pos

end
