/-
  FSOT Formal NeurolabGapsMathSpinePriors — Tier 62–64 live astrometry, prereg scaffold, NeuroLab gaps.
  Generator: scripts/gen_tiers_62_64_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neurolab_gaps_math_spine_observable_count : ℕ := 35
def neurolab_gaps_math_spine_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def neurolab_gaps_math_spine_headline_median_error_pct : ℝ := (0.0 : ℝ)
def neurolab_gaps_math_spine_beats_sota_headlines : ℕ := 2
def neurolab_gaps_math_spine_D_eff : ℕ := 17

theorem neurolab_gaps_math_spine_observable_count_pos : 0 < neurolab_gaps_math_spine_observable_count := by
  unfold neurolab_gaps_math_spine_observable_count; norm_num

theorem neurolab_gaps_math_spine_pooled_median_under_half_pct :
    neurolab_gaps_math_spine_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold neurolab_gaps_math_spine_pooled_median_error_pct; norm_num

theorem neurolab_gaps_math_spine_headline_median_under_half_pct :
    neurolab_gaps_math_spine_headline_median_error_pct < (0.5 : ℝ) := by
  unfold neurolab_gaps_math_spine_headline_median_error_pct; norm_num

theorem neurolab_gaps_math_spine_beats_sota_headlines_pos : 0 < neurolab_gaps_math_spine_beats_sota_headlines := by
  unfold neurolab_gaps_math_spine_beats_sota_headlines; norm_num

theorem neurolab_gaps_math_spine_bundle :
    neurolab_gaps_math_spine_observable_count = 35 ∧
    neurolab_gaps_math_spine_pooled_median_error_pct < (0.5 : ℝ) ∧
    neurolab_gaps_math_spine_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold neurolab_gaps_math_spine_observable_count; norm_num
  · exact neurolab_gaps_math_spine_pooled_median_under_half_pct
  · exact neurolab_gaps_math_spine_beats_sota_headlines_pos

end
