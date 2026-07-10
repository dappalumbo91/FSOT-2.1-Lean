/-
  FSOT Formal InitiationTransformationArchetypePriors — Tier 67 per-channel formula precision.
  Generator: scripts/gen_tiers_67_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def initiation_transformation_archetype_observable_count : ℕ := 10
def initiation_transformation_archetype_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def initiation_transformation_archetype_headline_median_error_pct : ℝ := (0.19339831498352392 : ℝ)
def initiation_transformation_archetype_beats_sota_headlines : ℕ := 2
def initiation_transformation_archetype_D_eff : ℕ := 17

theorem initiation_transformation_archetype_observable_count_pos : 0 < initiation_transformation_archetype_observable_count := by
  unfold initiation_transformation_archetype_observable_count; norm_num

theorem initiation_transformation_archetype_pooled_median_under_half_pct :
    initiation_transformation_archetype_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold initiation_transformation_archetype_pooled_median_error_pct; norm_num

theorem initiation_transformation_archetype_headline_median_under_half_pct :
    initiation_transformation_archetype_headline_median_error_pct < (0.5 : ℝ) := by
  unfold initiation_transformation_archetype_headline_median_error_pct; norm_num

theorem initiation_transformation_archetype_beats_sota_headlines_pos : 0 < initiation_transformation_archetype_beats_sota_headlines := by
  unfold initiation_transformation_archetype_beats_sota_headlines; norm_num

theorem initiation_transformation_archetype_bundle :
    initiation_transformation_archetype_observable_count = 10 ∧
    initiation_transformation_archetype_pooled_median_error_pct < (0.5 : ℝ) ∧
    initiation_transformation_archetype_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold initiation_transformation_archetype_observable_count; norm_num
  · exact initiation_transformation_archetype_pooled_median_under_half_pct
  · exact initiation_transformation_archetype_beats_sota_headlines_pos

end
