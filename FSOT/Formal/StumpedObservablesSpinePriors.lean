/-
  FSOT Formal StumpedObservablesSpinePriors — Stumped_Observables_Spine Tier 51 stumped observables spine.
  Generator: scripts/gen_stumped_observables_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def stumped_spine_observable_count : ℕ := 5
def stumped_spine_pooled_median_error_pct : ℝ := (0.042611 : ℝ)
def stumped_spine_headline_median_error_pct : ℝ := (0.042611 : ℝ)
def stumped_spine_beats_sota_headlines : ℕ := 2
def stumped_spine_D_eff : ℕ := 25
def stumped_spine_h0_sector_count : ℕ := 6
def stumped_spine_open_prediction_count : ℕ := 5

theorem stumped_spine_observable_count_pos : 0 < stumped_spine_observable_count := by
  unfold stumped_spine_observable_count; norm_num

theorem stumped_spine_pooled_median_under_half_pct :
    stumped_spine_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold stumped_spine_pooled_median_error_pct; norm_num

theorem stumped_spine_headline_median_under_half_pct :
    stumped_spine_headline_median_error_pct < (0.5 : ℝ) := by
  unfold stumped_spine_headline_median_error_pct; norm_num

theorem stumped_spine_beats_sota_headlines_pos : 0 < stumped_spine_beats_sota_headlines := by
  unfold stumped_spine_beats_sota_headlines; norm_num
theorem stumped_spine_spine_sectors_pos : 0 < stumped_spine_h0_sector_count := by unfold stumped_spine_h0_sector_count; norm_num

theorem stumped_spine_bundle :
    stumped_spine_observable_count = 5 ∧
    stumped_spine_pooled_median_error_pct < (0.5 : ℝ) ∧
    stumped_spine_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold stumped_spine_observable_count; norm_num
  · exact stumped_spine_pooled_median_under_half_pct
  · exact stumped_spine_beats_sota_headlines_pos

end
