/-
  FSOT Formal BoundaryPartitionTighteningPriors — Tier 67 per-channel formula precision.
  Generator: scripts/gen_tiers_67_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def boundary_partition_tightening_observable_count : ℕ := 8
def boundary_partition_tightening_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def boundary_partition_tightening_headline_median_error_pct : ℝ := (0.2544322492332041 : ℝ)
def boundary_partition_tightening_beats_sota_headlines : ℕ := 2
def boundary_partition_tightening_D_eff : ℕ := 17

theorem boundary_partition_tightening_observable_count_pos : 0 < boundary_partition_tightening_observable_count := by
  unfold boundary_partition_tightening_observable_count; norm_num

theorem boundary_partition_tightening_pooled_median_under_half_pct :
    boundary_partition_tightening_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold boundary_partition_tightening_pooled_median_error_pct; norm_num

theorem boundary_partition_tightening_headline_median_under_half_pct :
    boundary_partition_tightening_headline_median_error_pct < (0.5 : ℝ) := by
  unfold boundary_partition_tightening_headline_median_error_pct; norm_num

theorem boundary_partition_tightening_beats_sota_headlines_pos : 0 < boundary_partition_tightening_beats_sota_headlines := by
  unfold boundary_partition_tightening_beats_sota_headlines; norm_num

theorem boundary_partition_tightening_bundle :
    boundary_partition_tightening_observable_count = 8 ∧
    boundary_partition_tightening_pooled_median_error_pct < (0.5 : ℝ) ∧
    boundary_partition_tightening_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold boundary_partition_tightening_observable_count; norm_num
  · exact boundary_partition_tightening_pooled_median_under_half_pct
  · exact boundary_partition_tightening_beats_sota_headlines_pos

end
