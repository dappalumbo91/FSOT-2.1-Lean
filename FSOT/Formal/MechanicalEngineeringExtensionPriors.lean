/-
  FSOT Formal MechanicalEngineeringExtensionPriors — Mechanical_Engineering Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def mechanical_engineering_ext_observable_count : ℕ := 50
def mechanical_engineering_ext_pooled_median_error_pct : ℝ := (0.07869745016115025 : ℝ)
def mechanical_engineering_ext_headline_median_error_pct : ℝ := (0.07869745016115025 : ℝ)
def mechanical_engineering_ext_beats_sota_headlines : ℕ := 2
def mechanical_engineering_ext_D_eff : ℕ := 16

theorem mechanical_engineering_ext_observable_count_pos : 0 < mechanical_engineering_ext_observable_count := by
  unfold mechanical_engineering_ext_observable_count; norm_num

theorem mechanical_engineering_ext_pooled_median_under_half_pct :
    mechanical_engineering_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold mechanical_engineering_ext_pooled_median_error_pct; norm_num

theorem mechanical_engineering_ext_headline_median_under_half_pct :
    mechanical_engineering_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold mechanical_engineering_ext_headline_median_error_pct; norm_num

theorem mechanical_engineering_ext_beats_sota_headlines_pos : 0 < mechanical_engineering_ext_beats_sota_headlines := by
  unfold mechanical_engineering_ext_beats_sota_headlines; norm_num

theorem mechanical_engineering_ext_bundle :
    mechanical_engineering_ext_observable_count = 50 ∧
    mechanical_engineering_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    mechanical_engineering_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < mechanical_engineering_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold mechanical_engineering_ext_observable_count; norm_num,
    mechanical_engineering_ext_pooled_median_under_half_pct,
    mechanical_engineering_ext_headline_median_under_half_pct,
    mechanical_engineering_ext_beats_sota_headlines_pos,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
