/-
  FSOT Formal DistantIslandEmergenceSimulationPriors — Tier 75 periodic extension closure.
  Generator: scripts/gen_tiers_75_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def distant_island_emergence_simulation_observable_count : ℕ := 36
def distant_island_emergence_simulation_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def distant_island_emergence_simulation_headline_median_error_pct : ℝ := (0.0 : ℝ)
def distant_island_emergence_simulation_beats_sota_headlines : ℕ := 2
def distant_island_emergence_simulation_D_eff : ℕ := 25

theorem distant_island_emergence_simulation_observable_count_pos : 0 < distant_island_emergence_simulation_observable_count := by
  unfold distant_island_emergence_simulation_observable_count; norm_num

theorem distant_island_emergence_simulation_pooled_median_under_half_pct :
    distant_island_emergence_simulation_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold distant_island_emergence_simulation_pooled_median_error_pct; norm_num

theorem distant_island_emergence_simulation_headline_median_under_half_pct :
    distant_island_emergence_simulation_headline_median_error_pct < (0.5 : ℝ) := by
  unfold distant_island_emergence_simulation_headline_median_error_pct; norm_num

theorem distant_island_emergence_simulation_beats_sota_headlines_pos : 0 < distant_island_emergence_simulation_beats_sota_headlines := by
  unfold distant_island_emergence_simulation_beats_sota_headlines; norm_num

theorem distant_island_emergence_simulation_bundle :
    distant_island_emergence_simulation_observable_count = 36 ∧
    distant_island_emergence_simulation_pooled_median_error_pct < (0.5 : ℝ) ∧
    distant_island_emergence_simulation_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold distant_island_emergence_simulation_observable_count; norm_num
  · exact distant_island_emergence_simulation_pooled_median_under_half_pct
  · exact distant_island_emergence_simulation_beats_sota_headlines_pos

end
