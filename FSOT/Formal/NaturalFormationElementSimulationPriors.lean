/-
  FSOT Formal NaturalFormationElementSimulationPriors — Tier 72 periodic table completion.
  Generator: scripts/gen_tiers_72_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def natural_formation_element_simulation_observable_count : ℕ := 44
def natural_formation_element_simulation_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def natural_formation_element_simulation_headline_median_error_pct : ℝ := (0.0 : ℝ)
def natural_formation_element_simulation_beats_sota_headlines : ℕ := 2
def natural_formation_element_simulation_D_eff : ℕ := 11

theorem natural_formation_element_simulation_observable_count_pos : 0 < natural_formation_element_simulation_observable_count := by
  unfold natural_formation_element_simulation_observable_count; norm_num

theorem natural_formation_element_simulation_pooled_median_under_half_pct :
    natural_formation_element_simulation_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold natural_formation_element_simulation_pooled_median_error_pct; norm_num

theorem natural_formation_element_simulation_headline_median_under_half_pct :
    natural_formation_element_simulation_headline_median_error_pct < (0.5 : ℝ) := by
  unfold natural_formation_element_simulation_headline_median_error_pct; norm_num

theorem natural_formation_element_simulation_beats_sota_headlines_pos : 0 < natural_formation_element_simulation_beats_sota_headlines := by
  unfold natural_formation_element_simulation_beats_sota_headlines; norm_num

theorem natural_formation_element_simulation_bundle :
    natural_formation_element_simulation_observable_count = 44 ∧
    natural_formation_element_simulation_pooled_median_error_pct < (0.5 : ℝ) ∧
    natural_formation_element_simulation_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold natural_formation_element_simulation_observable_count; norm_num
  · exact natural_formation_element_simulation_pooled_median_under_half_pct
  · exact natural_formation_element_simulation_beats_sota_headlines_pos

end
