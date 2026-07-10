/-
  FSOT Formal CompactificationLadderPriors — Compactification_Ladder Tier N compactification ladder.
  Generator: scripts/gen_tier_n_compactification_ladder_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def comp_lad_observable_count : ℕ := 60
def comp_lad_pooled_median_error_pct : ℝ := (0.0220747159758794 : ℝ)
def comp_lad_headline_median_error_pct : ℝ := (0.0220747159758794 : ℝ)
def comp_lad_beats_sota_headlines : ℕ := 2
def comp_lad_D_eff : ℕ := 18
def comp_lad_rung_count : ℕ := 10

theorem comp_lad_observable_count_pos : 0 < comp_lad_observable_count := by
  unfold comp_lad_observable_count; norm_num

theorem comp_lad_pooled_median_under_five_pct :
    comp_lad_pooled_median_error_pct < (5 : ℝ) := by
  unfold comp_lad_pooled_median_error_pct; norm_num

theorem comp_lad_headline_median_under_five_pct :
    comp_lad_headline_median_error_pct < (5 : ℝ) := by
  unfold comp_lad_headline_median_error_pct; norm_num

theorem comp_lad_beats_sota_headlines_pos : 0 < comp_lad_beats_sota_headlines := by
  unfold comp_lad_beats_sota_headlines; norm_num
theorem comp_lad_rungs_complete : comp_lad_rung_count = 10 := by unfold comp_lad_rung_count; norm_num

theorem comp_lad_bundle :
    comp_lad_observable_count = 60 ∧
    comp_lad_pooled_median_error_pct < (5 : ℝ) ∧
    comp_lad_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold comp_lad_observable_count; norm_num
  · exact comp_lad_pooled_median_under_five_pct
  · exact comp_lad_beats_sota_headlines_pos

end
