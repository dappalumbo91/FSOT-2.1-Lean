/-
  FSOT Formal MaterialPropertyVerificationScaffoldPriors — Tier 59/60 public material/fuel scaffold + live astrometry.
  Generator: scripts/gen_tiers_59_60_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def material_property_verification_scaffold_observable_count : ℕ := 79
def material_property_verification_scaffold_pooled_median_error_pct : ℝ := (0.002271 : ℝ)
def material_property_verification_scaffold_headline_median_error_pct : ℝ := (0.002647 : ℝ)
def material_property_verification_scaffold_beats_sota_headlines : ℕ := 2
def material_property_verification_scaffold_D_eff : ℕ := 15

theorem material_property_verification_scaffold_observable_count_pos : 0 < material_property_verification_scaffold_observable_count := by
  unfold material_property_verification_scaffold_observable_count; norm_num

theorem material_property_verification_scaffold_pooled_median_under_half_pct :
    material_property_verification_scaffold_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold material_property_verification_scaffold_pooled_median_error_pct; norm_num

theorem material_property_verification_scaffold_headline_median_under_half_pct :
    material_property_verification_scaffold_headline_median_error_pct < (0.5 : ℝ) := by
  unfold material_property_verification_scaffold_headline_median_error_pct; norm_num

theorem material_property_verification_scaffold_beats_sota_headlines_pos : 0 < material_property_verification_scaffold_beats_sota_headlines := by
  unfold material_property_verification_scaffold_beats_sota_headlines; norm_num

theorem material_property_verification_scaffold_bundle :
    material_property_verification_scaffold_observable_count = 79 ∧
    material_property_verification_scaffold_pooled_median_error_pct < (0.5 : ℝ) ∧
    material_property_verification_scaffold_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold material_property_verification_scaffold_observable_count; norm_num
  · exact material_property_verification_scaffold_pooled_median_under_half_pct
  · exact material_property_verification_scaffold_beats_sota_headlines_pos

end
