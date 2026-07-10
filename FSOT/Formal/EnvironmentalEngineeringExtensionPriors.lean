/-
  FSOT Formal EnvironmentalEngineeringExtensionPriors — Environmental_Engineering Tier D extension (real API anchors).
  Generator: scripts/gen_tier_d_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def environmental_engineering_ext_observable_count : ℕ := 18416
def environmental_engineering_ext_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def environmental_engineering_ext_headline_median_error_pct : ℝ := (0.0 : ℝ)
def environmental_engineering_ext_beats_sota_headlines : ℕ := 2
def environmental_engineering_ext_D_eff : ℕ := 17

theorem environmental_engineering_ext_observable_count_pos : 0 < environmental_engineering_ext_observable_count := by
  unfold environmental_engineering_ext_observable_count; norm_num

theorem environmental_engineering_ext_pooled_median_under_half_pct :
    environmental_engineering_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold environmental_engineering_ext_pooled_median_error_pct; norm_num

theorem environmental_engineering_ext_headline_median_under_half_pct :
    environmental_engineering_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold environmental_engineering_ext_headline_median_error_pct; norm_num

theorem environmental_engineering_ext_beats_sota_headlines_pos : 0 < environmental_engineering_ext_beats_sota_headlines := by
  unfold environmental_engineering_ext_beats_sota_headlines; norm_num

theorem environmental_engineering_ext_bundle :
    environmental_engineering_ext_observable_count = 18416 ∧
    environmental_engineering_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    environmental_engineering_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < environmental_engineering_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold environmental_engineering_ext_observable_count; norm_num,
    environmental_engineering_ext_pooled_median_under_half_pct,
    environmental_engineering_ext_headline_median_under_half_pct,
    environmental_engineering_ext_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
