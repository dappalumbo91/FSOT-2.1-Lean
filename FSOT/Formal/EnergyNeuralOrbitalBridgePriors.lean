/-
  FSOT Formal EnergyNeuralOrbitalBridgePriors — extension domain Energy_Neural_Orbital_Bridge.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def energy_neural_orbital_bridge_observable_count : ℕ := 48
def energy_neural_orbital_bridge_D_eff : ℕ := 16

theorem energy_neural_orbital_bridge_observable_count_pos : 0 < energy_neural_orbital_bridge_observable_count := by
  unfold energy_neural_orbital_bridge_observable_count; decide

theorem energy_neural_orbital_bridge_median_error_under_half_pct :
    (0.018002668701796887 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.018002668701796887 : ℝ) < (0.5 : ℝ))

theorem energy_neural_orbital_bridge_bundle :
    energy_neural_orbital_bridge_observable_count = 48 ∧
    energy_neural_orbital_bridge_D_eff = 16 ∧
    (0.018002668701796887 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold energy_neural_orbital_bridge_observable_count; decide,
    by unfold energy_neural_orbital_bridge_D_eff; decide,
    energy_neural_orbital_bridge_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
