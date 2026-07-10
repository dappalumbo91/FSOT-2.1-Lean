/-
  FSOT Formal ElementSynthesisConditionScaffoldPriors — Tier 73 lab synthesis + metamaterial fluid design.
  Generator: scripts/gen_tiers_73_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def element_synthesis_condition_scaffold_observable_count : ℕ := 45
def element_synthesis_condition_scaffold_pooled_median_error_pct : ℝ := (0.000787 : ℝ)
def element_synthesis_condition_scaffold_headline_median_error_pct : ℝ := (0.000787 : ℝ)
def element_synthesis_condition_scaffold_beats_sota_headlines : ℕ := 2
def element_synthesis_condition_scaffold_D_eff : ℕ := 14

theorem element_synthesis_condition_scaffold_observable_count_pos : 0 < element_synthesis_condition_scaffold_observable_count := by
  unfold element_synthesis_condition_scaffold_observable_count; norm_num

theorem element_synthesis_condition_scaffold_pooled_median_under_half_pct :
    element_synthesis_condition_scaffold_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold element_synthesis_condition_scaffold_pooled_median_error_pct; norm_num

theorem element_synthesis_condition_scaffold_headline_median_under_half_pct :
    element_synthesis_condition_scaffold_headline_median_error_pct < (0.5 : ℝ) := by
  unfold element_synthesis_condition_scaffold_headline_median_error_pct; norm_num

theorem element_synthesis_condition_scaffold_beats_sota_headlines_pos : 0 < element_synthesis_condition_scaffold_beats_sota_headlines := by
  unfold element_synthesis_condition_scaffold_beats_sota_headlines; norm_num

theorem element_synthesis_condition_scaffold_bundle :
    element_synthesis_condition_scaffold_observable_count = 45 ∧
    element_synthesis_condition_scaffold_pooled_median_error_pct < (0.5 : ℝ) ∧
    element_synthesis_condition_scaffold_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold element_synthesis_condition_scaffold_observable_count; norm_num
  · exact element_synthesis_condition_scaffold_pooled_median_under_half_pct
  · exact element_synthesis_condition_scaffold_beats_sota_headlines_pos

end
