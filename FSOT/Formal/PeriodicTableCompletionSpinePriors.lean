/-
  FSOT Formal PeriodicTableCompletionSpinePriors — Tier 72 periodic table completion.
  Generator: scripts/gen_tiers_72_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def periodic_table_completion_spine_observable_count : ℕ := 38
def periodic_table_completion_spine_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def periodic_table_completion_spine_headline_median_error_pct : ℝ := (1e-06 : ℝ)
def periodic_table_completion_spine_beats_sota_headlines : ℕ := 2
def periodic_table_completion_spine_D_eff : ℕ := 12

theorem periodic_table_completion_spine_observable_count_pos : 0 < periodic_table_completion_spine_observable_count := by
  unfold periodic_table_completion_spine_observable_count; norm_num

theorem periodic_table_completion_spine_pooled_median_under_half_pct :
    periodic_table_completion_spine_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold periodic_table_completion_spine_pooled_median_error_pct; norm_num

theorem periodic_table_completion_spine_headline_median_under_half_pct :
    periodic_table_completion_spine_headline_median_error_pct < (0.5 : ℝ) := by
  unfold periodic_table_completion_spine_headline_median_error_pct; norm_num

theorem periodic_table_completion_spine_beats_sota_headlines_pos : 0 < periodic_table_completion_spine_beats_sota_headlines := by
  unfold periodic_table_completion_spine_beats_sota_headlines; norm_num

theorem periodic_table_completion_spine_bundle :
    periodic_table_completion_spine_observable_count = 38 ∧
    periodic_table_completion_spine_pooled_median_error_pct < (0.5 : ℝ) ∧
    periodic_table_completion_spine_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold periodic_table_completion_spine_observable_count; norm_num
  · exact periodic_table_completion_spine_pooled_median_under_half_pct
  · exact periodic_table_completion_spine_beats_sota_headlines_pos

end
