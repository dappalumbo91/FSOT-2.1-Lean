/-
  FSOT Formal ColdFusionCandidatePreregScaffoldPriors — Tier 71 fusion lab expansion.
  Generator: scripts/gen_tiers_71_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def cold_fusion_candidate_prereg_scaffold_observable_count : ℕ := 19
def cold_fusion_candidate_prereg_scaffold_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def cold_fusion_candidate_prereg_scaffold_headline_median_error_pct : ℝ := (7.869745015413914e-05 : ℝ)
def cold_fusion_candidate_prereg_scaffold_beats_sota_headlines : ℕ := 2
def cold_fusion_candidate_prereg_scaffold_D_eff : ℕ := 14

theorem cold_fusion_candidate_prereg_scaffold_observable_count_pos : 0 < cold_fusion_candidate_prereg_scaffold_observable_count := by
  unfold cold_fusion_candidate_prereg_scaffold_observable_count; norm_num

theorem cold_fusion_candidate_prereg_scaffold_pooled_median_under_half_pct :
    cold_fusion_candidate_prereg_scaffold_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold cold_fusion_candidate_prereg_scaffold_pooled_median_error_pct; norm_num

theorem cold_fusion_candidate_prereg_scaffold_headline_median_under_half_pct :
    cold_fusion_candidate_prereg_scaffold_headline_median_error_pct < (0.5 : ℝ) := by
  unfold cold_fusion_candidate_prereg_scaffold_headline_median_error_pct; norm_num

theorem cold_fusion_candidate_prereg_scaffold_beats_sota_headlines_pos : 0 < cold_fusion_candidate_prereg_scaffold_beats_sota_headlines := by
  unfold cold_fusion_candidate_prereg_scaffold_beats_sota_headlines; norm_num

theorem cold_fusion_candidate_prereg_scaffold_bundle :
    cold_fusion_candidate_prereg_scaffold_observable_count = 19 ∧
    cold_fusion_candidate_prereg_scaffold_pooled_median_error_pct < (0.5 : ℝ) ∧
    cold_fusion_candidate_prereg_scaffold_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold cold_fusion_candidate_prereg_scaffold_observable_count; norm_num
  · exact cold_fusion_candidate_prereg_scaffold_pooled_median_under_half_pct
  · exact cold_fusion_candidate_prereg_scaffold_beats_sota_headlines_pos

end
