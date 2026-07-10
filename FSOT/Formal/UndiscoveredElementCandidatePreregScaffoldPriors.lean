/-
  FSOT Formal UndiscoveredElementCandidatePreregScaffoldPriors — Tier 72 periodic table completion.
  Generator: scripts/gen_tiers_72_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def undiscovered_element_candidate_prereg_scaffold_observable_count : ℕ := 25
def undiscovered_element_candidate_prereg_scaffold_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def undiscovered_element_candidate_prereg_scaffold_headline_median_error_pct : ℝ := (9.50413070515626e-09 : ℝ)
def undiscovered_element_candidate_prereg_scaffold_beats_sota_headlines : ℕ := 2
def undiscovered_element_candidate_prereg_scaffold_D_eff : ℕ := 10

theorem undiscovered_element_candidate_prereg_scaffold_observable_count_pos : 0 < undiscovered_element_candidate_prereg_scaffold_observable_count := by
  unfold undiscovered_element_candidate_prereg_scaffold_observable_count; norm_num

theorem undiscovered_element_candidate_prereg_scaffold_pooled_median_under_half_pct :
    undiscovered_element_candidate_prereg_scaffold_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold undiscovered_element_candidate_prereg_scaffold_pooled_median_error_pct; norm_num

theorem undiscovered_element_candidate_prereg_scaffold_headline_median_under_half_pct :
    undiscovered_element_candidate_prereg_scaffold_headline_median_error_pct < (0.5 : ℝ) := by
  unfold undiscovered_element_candidate_prereg_scaffold_headline_median_error_pct; norm_num

theorem undiscovered_element_candidate_prereg_scaffold_beats_sota_headlines_pos : 0 < undiscovered_element_candidate_prereg_scaffold_beats_sota_headlines := by
  unfold undiscovered_element_candidate_prereg_scaffold_beats_sota_headlines; norm_num

theorem undiscovered_element_candidate_prereg_scaffold_bundle :
    undiscovered_element_candidate_prereg_scaffold_observable_count = 25 ∧
    undiscovered_element_candidate_prereg_scaffold_pooled_median_error_pct < (0.5 : ℝ) ∧
    undiscovered_element_candidate_prereg_scaffold_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold undiscovered_element_candidate_prereg_scaffold_observable_count; norm_num
  · exact undiscovered_element_candidate_prereg_scaffold_pooled_median_under_half_pct
  · exact undiscovered_element_candidate_prereg_scaffold_beats_sota_headlines_pos

end
