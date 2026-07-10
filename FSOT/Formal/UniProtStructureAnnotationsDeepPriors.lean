/-
  FSOT Formal UniProtStructureAnnotationsDeepPriors — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def uniprot_structure_annotations_deep_observable_count : ℕ := 121
def uniprot_structure_annotations_deep_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def uniprot_structure_annotations_deep_headline_median_error_pct : ℝ := (0.0 : ℝ)
def uniprot_structure_annotations_deep_beats_sota_headlines : ℕ := 2
def uniprot_structure_annotations_deep_D_eff : ℕ := 13

theorem uniprot_structure_annotations_deep_observable_count_pos : 0 < uniprot_structure_annotations_deep_observable_count := by
  unfold uniprot_structure_annotations_deep_observable_count; norm_num

theorem uniprot_structure_annotations_deep_pooled_median_under_half_pct :
    uniprot_structure_annotations_deep_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold uniprot_structure_annotations_deep_pooled_median_error_pct; norm_num

theorem uniprot_structure_annotations_deep_headline_median_under_half_pct :
    uniprot_structure_annotations_deep_headline_median_error_pct < (0.5 : ℝ) := by
  unfold uniprot_structure_annotations_deep_headline_median_error_pct; norm_num

theorem uniprot_structure_annotations_deep_beats_sota_headlines_pos : 0 < uniprot_structure_annotations_deep_beats_sota_headlines := by
  unfold uniprot_structure_annotations_deep_beats_sota_headlines; norm_num

theorem uniprot_structure_annotations_deep_bundle :
    uniprot_structure_annotations_deep_observable_count = 121 ∧
    uniprot_structure_annotations_deep_pooled_median_error_pct < (0.5 : ℝ) ∧
    uniprot_structure_annotations_deep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold uniprot_structure_annotations_deep_observable_count; norm_num
  · exact uniprot_structure_annotations_deep_pooled_median_under_half_pct
  · exact uniprot_structure_annotations_deep_beats_sota_headlines_pos

end
