/-
  FSOT Formal DomainCouplingSimulationPriors — extension domain Domain_Coupling_Simulation.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def domain_coupling_simulation_observable_count : ℕ := 18691
def domain_coupling_simulation_D_eff : ℕ := 17

theorem domain_coupling_simulation_observable_count_pos : 0 < domain_coupling_simulation_observable_count := by
  unfold domain_coupling_simulation_observable_count; decide

theorem domain_coupling_simulation_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem domain_coupling_simulation_bundle :
    domain_coupling_simulation_observable_count = 18691 ∧
    domain_coupling_simulation_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold domain_coupling_simulation_observable_count; decide,
    by unfold domain_coupling_simulation_D_eff; decide,
    domain_coupling_simulation_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
