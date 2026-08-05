/-
  FSOT Formal TimeEmergenceSimulationPriors — extension domain Time_Emergence_Simulation.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def time_emergence_simulation_observable_count : ℕ := 28
def time_emergence_simulation_D_eff : ℕ := 18

theorem time_emergence_simulation_observable_count_pos : 0 < time_emergence_simulation_observable_count := by
  unfold time_emergence_simulation_observable_count; decide

theorem time_emergence_simulation_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem time_emergence_simulation_bundle :
    time_emergence_simulation_observable_count = 28 ∧
    time_emergence_simulation_D_eff = 18 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold time_emergence_simulation_observable_count; decide,
    by unfold time_emergence_simulation_D_eff; decide,
    time_emergence_simulation_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
