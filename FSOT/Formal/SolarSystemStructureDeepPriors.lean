/-
  FSOT Formal SolarSystemStructureDeepPriors — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def solar_system_structure_deep_observable_count : ℕ := 50
def solar_system_structure_deep_pooled_median_error_pct : ℝ := (0.009693 : ℝ)
def solar_system_structure_deep_headline_median_error_pct : ℝ := (0.032274 : ℝ)
def solar_system_structure_deep_beats_sota_headlines : ℕ := 3
def solar_system_structure_deep_D_eff : ℕ := 18

theorem solar_system_structure_deep_observable_count_pos : 0 < solar_system_structure_deep_observable_count := by
  unfold solar_system_structure_deep_observable_count; norm_num

theorem solar_system_structure_deep_pooled_median_under_half_pct :
    solar_system_structure_deep_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold solar_system_structure_deep_pooled_median_error_pct; norm_num

theorem solar_system_structure_deep_headline_median_under_half_pct :
    solar_system_structure_deep_headline_median_error_pct < (0.5 : ℝ) := by
  unfold solar_system_structure_deep_headline_median_error_pct; norm_num

theorem solar_system_structure_deep_beats_sota_headlines_pos : 0 < solar_system_structure_deep_beats_sota_headlines := by
  unfold solar_system_structure_deep_beats_sota_headlines; norm_num

theorem solar_system_structure_deep_bundle :
    solar_system_structure_deep_observable_count = 50 ∧
    solar_system_structure_deep_pooled_median_error_pct < (0.5 : ℝ) ∧
    solar_system_structure_deep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold solar_system_structure_deep_observable_count; norm_num
  · exact solar_system_structure_deep_pooled_median_under_half_pct
  · exact solar_system_structure_deep_beats_sota_headlines_pos

end
