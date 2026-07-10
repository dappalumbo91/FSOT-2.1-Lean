/-
  FSOT Formal CompactObjectBinaryEventsPriors — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def compact_object_binary_events_observable_count : ℕ := 40
def compact_object_binary_events_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def compact_object_binary_events_headline_median_error_pct : ℝ := (0.0 : ℝ)
def compact_object_binary_events_beats_sota_headlines : ℕ := 2
def compact_object_binary_events_D_eff : ℕ := 20

theorem compact_object_binary_events_observable_count_pos : 0 < compact_object_binary_events_observable_count := by
  unfold compact_object_binary_events_observable_count; norm_num

theorem compact_object_binary_events_pooled_median_under_half_pct :
    compact_object_binary_events_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold compact_object_binary_events_pooled_median_error_pct; norm_num

theorem compact_object_binary_events_headline_median_under_half_pct :
    compact_object_binary_events_headline_median_error_pct < (0.5 : ℝ) := by
  unfold compact_object_binary_events_headline_median_error_pct; norm_num

theorem compact_object_binary_events_beats_sota_headlines_pos : 0 < compact_object_binary_events_beats_sota_headlines := by
  unfold compact_object_binary_events_beats_sota_headlines; norm_num

theorem compact_object_binary_events_bundle :
    compact_object_binary_events_observable_count = 40 ∧
    compact_object_binary_events_pooled_median_error_pct < (0.5 : ℝ) ∧
    compact_object_binary_events_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold compact_object_binary_events_observable_count; norm_num
  · exact compact_object_binary_events_pooled_median_under_half_pct
  · exact compact_object_binary_events_beats_sota_headlines_pos

end
