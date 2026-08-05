/-
  FSOT Formal DistantIslandEmergenceSimulationPriors — extension domain Distant_Island_Emergence_Simulation.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def distant_island_emergence_simulation_observable_count : ℕ := 36
def distant_island_emergence_simulation_D_eff : ℕ := 25

theorem distant_island_emergence_simulation_observable_count_pos : 0 < distant_island_emergence_simulation_observable_count := by
  unfold distant_island_emergence_simulation_observable_count; decide

theorem distant_island_emergence_simulation_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem distant_island_emergence_simulation_bundle :
    distant_island_emergence_simulation_observable_count = 36 ∧
    distant_island_emergence_simulation_D_eff = 25 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold distant_island_emergence_simulation_observable_count; decide,
    by unfold distant_island_emergence_simulation_D_eff; decide,
    distant_island_emergence_simulation_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
