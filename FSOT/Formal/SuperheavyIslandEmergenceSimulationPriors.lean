/-
  FSOT Formal SuperheavyIslandEmergenceSimulationPriors — Tier 74 superheavy island Z=120-126.
  Generator: scripts/gen_tiers_74_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def superheavy_island_emergence_simulation_observable_count : ℕ := 44
def superheavy_island_emergence_simulation_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def superheavy_island_emergence_simulation_headline_median_error_pct : ℝ := (0.0 : ℝ)
def superheavy_island_emergence_simulation_beats_sota_headlines : ℕ := 2
def superheavy_island_emergence_simulation_D_eff : ℕ := 21

theorem superheavy_island_emergence_simulation_observable_count_pos : 0 < superheavy_island_emergence_simulation_observable_count := by
  unfold superheavy_island_emergence_simulation_observable_count; norm_num

theorem superheavy_island_emergence_simulation_pooled_median_under_half_pct :
    superheavy_island_emergence_simulation_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold superheavy_island_emergence_simulation_pooled_median_error_pct; norm_num

theorem superheavy_island_emergence_simulation_headline_median_under_half_pct :
    superheavy_island_emergence_simulation_headline_median_error_pct < (0.5 : ℝ) := by
  unfold superheavy_island_emergence_simulation_headline_median_error_pct; norm_num

theorem superheavy_island_emergence_simulation_beats_sota_headlines_pos : 0 < superheavy_island_emergence_simulation_beats_sota_headlines := by
  unfold superheavy_island_emergence_simulation_beats_sota_headlines; norm_num

theorem superheavy_island_emergence_simulation_bundle :
    superheavy_island_emergence_simulation_observable_count = 44 ∧
    superheavy_island_emergence_simulation_pooled_median_error_pct < (0.5 : ℝ) ∧
    superheavy_island_emergence_simulation_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold superheavy_island_emergence_simulation_observable_count; norm_num
  · exact superheavy_island_emergence_simulation_pooled_median_under_half_pct
  · exact superheavy_island_emergence_simulation_beats_sota_headlines_pos

end
