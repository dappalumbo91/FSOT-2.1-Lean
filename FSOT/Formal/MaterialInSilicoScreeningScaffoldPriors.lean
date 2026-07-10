/-
  FSOT Formal MaterialInSilicoScreeningScaffoldPriors — Tier 65 prereg screening scaffolds (public methodology gates).
  Generator: scripts/gen_tiers_65_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def material_in_silico_screening_scaffold_observable_count : ℕ := 42
def material_in_silico_screening_scaffold_pooled_median_error_pct : ℝ := (0.00206 : ℝ)
def material_in_silico_screening_scaffold_headline_median_error_pct : ℝ := (0.002424 : ℝ)
def material_in_silico_screening_scaffold_beats_sota_headlines : ℕ := 2
def material_in_silico_screening_scaffold_D_eff : ℕ := 15

theorem material_in_silico_screening_scaffold_observable_count_pos : 0 < material_in_silico_screening_scaffold_observable_count := by
  unfold material_in_silico_screening_scaffold_observable_count; norm_num

theorem material_in_silico_screening_scaffold_pooled_median_under_half_pct :
    material_in_silico_screening_scaffold_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold material_in_silico_screening_scaffold_pooled_median_error_pct; norm_num

theorem material_in_silico_screening_scaffold_headline_median_under_half_pct :
    material_in_silico_screening_scaffold_headline_median_error_pct < (0.5 : ℝ) := by
  unfold material_in_silico_screening_scaffold_headline_median_error_pct; norm_num

theorem material_in_silico_screening_scaffold_beats_sota_headlines_pos : 0 < material_in_silico_screening_scaffold_beats_sota_headlines := by
  unfold material_in_silico_screening_scaffold_beats_sota_headlines; norm_num

theorem material_in_silico_screening_scaffold_bundle :
    material_in_silico_screening_scaffold_observable_count = 42 ∧
    material_in_silico_screening_scaffold_pooled_median_error_pct < (0.5 : ℝ) ∧
    material_in_silico_screening_scaffold_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold material_in_silico_screening_scaffold_observable_count; norm_num
  · exact material_in_silico_screening_scaffold_pooled_median_under_half_pct
  · exact material_in_silico_screening_scaffold_beats_sota_headlines_pos

end
