/-
  FSOT Formal LiveIngestSpinePriors — Tier 68–70 expansion.
  Generator: scripts/gen_tiers_68_70_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def live_ingest_spine_observable_count : ℕ := 28
def live_ingest_spine_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def live_ingest_spine_headline_median_error_pct : ℝ := (0.0 : ℝ)
def live_ingest_spine_beats_sota_headlines : ℕ := 2
def live_ingest_spine_D_eff : ℕ := 17

theorem live_ingest_spine_observable_count_pos : 0 < live_ingest_spine_observable_count := by
  unfold live_ingest_spine_observable_count; norm_num

theorem live_ingest_spine_pooled_median_under_half_pct :
    live_ingest_spine_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold live_ingest_spine_pooled_median_error_pct; norm_num

theorem live_ingest_spine_headline_median_under_half_pct :
    live_ingest_spine_headline_median_error_pct < (0.5 : ℝ) := by
  unfold live_ingest_spine_headline_median_error_pct; norm_num

theorem live_ingest_spine_beats_sota_headlines_pos : 0 < live_ingest_spine_beats_sota_headlines := by
  unfold live_ingest_spine_beats_sota_headlines; norm_num

theorem live_ingest_spine_bundle :
    live_ingest_spine_observable_count = 28 ∧
    live_ingest_spine_pooled_median_error_pct < (0.5 : ℝ) ∧
    live_ingest_spine_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold live_ingest_spine_observable_count; norm_num
  · exact live_ingest_spine_pooled_median_under_half_pct
  · exact live_ingest_spine_beats_sota_headlines_pos

end
