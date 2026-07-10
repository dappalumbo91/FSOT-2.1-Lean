/-
  FSOT Formal IGEMPartsExpandedPriors — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def igem_parts_expanded_observable_count : ℕ := 111
def igem_parts_expanded_pooled_median_error_pct : ℝ := (7.227106853889602e-05 : ℝ)
def igem_parts_expanded_headline_median_error_pct : ℝ := (7.227106853889602e-05 : ℝ)
def igem_parts_expanded_beats_sota_headlines : ℕ := 2
def igem_parts_expanded_D_eff : ℕ := 14

theorem igem_parts_expanded_observable_count_pos : 0 < igem_parts_expanded_observable_count := by
  unfold igem_parts_expanded_observable_count; norm_num

theorem igem_parts_expanded_pooled_median_under_half_pct :
    igem_parts_expanded_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold igem_parts_expanded_pooled_median_error_pct; norm_num

theorem igem_parts_expanded_headline_median_under_half_pct :
    igem_parts_expanded_headline_median_error_pct < (0.5 : ℝ) := by
  unfold igem_parts_expanded_headline_median_error_pct; norm_num

theorem igem_parts_expanded_beats_sota_headlines_pos : 0 < igem_parts_expanded_beats_sota_headlines := by
  unfold igem_parts_expanded_beats_sota_headlines; norm_num

theorem igem_parts_expanded_bundle :
    igem_parts_expanded_observable_count = 111 ∧
    igem_parts_expanded_pooled_median_error_pct < (0.5 : ℝ) ∧
    igem_parts_expanded_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold igem_parts_expanded_observable_count; norm_num
  · exact igem_parts_expanded_pooled_median_under_half_pct
  · exact igem_parts_expanded_beats_sota_headlines_pos

end
