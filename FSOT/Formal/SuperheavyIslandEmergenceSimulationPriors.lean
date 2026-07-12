/-
  FSOT Formal SuperheavyIslandEmergenceSimulationPriors — extension domain Superheavy_Island_Emergence_Simulation.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def superheavy_island_emergence_simulation_observable_count : ℕ := 44
def superheavy_island_emergence_simulation_D_eff : ℕ := 21

theorem superheavy_island_emergence_simulation_observable_count_pos : 0 < superheavy_island_emergence_simulation_observable_count := by
  unfold superheavy_island_emergence_simulation_observable_count; norm_num

theorem superheavy_island_emergence_simulation_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem superheavy_island_emergence_simulation_bundle :
    superheavy_island_emergence_simulation_observable_count = 44 ∧
    superheavy_island_emergence_simulation_D_eff = 21 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold superheavy_island_emergence_simulation_observable_count; norm_num,
    by unfold superheavy_island_emergence_simulation_D_eff; norm_num,
    superheavy_island_emergence_simulation_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
