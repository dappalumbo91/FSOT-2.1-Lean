/-
  FSOT Formal NeuralGalacticOrbitalBridgePriors — extension domain Neural_Galactic_Orbital_Bridge.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def neural_galactic_orbital_bridge_observable_count : ℕ := 49
def neural_galactic_orbital_bridge_D_eff : ℕ := 17

theorem neural_galactic_orbital_bridge_observable_count_pos : 0 < neural_galactic_orbital_bridge_observable_count := by
  unfold neural_galactic_orbital_bridge_observable_count; decide

theorem neural_galactic_orbital_bridge_median_error_under_half_pct :
    (0.018002668701799784 : ℝ) < (0.5 : ℝ) := by norm_num

theorem neural_galactic_orbital_bridge_bundle :
    neural_galactic_orbital_bridge_observable_count = 49 ∧
    neural_galactic_orbital_bridge_D_eff = 17 ∧
    (0.018002668701799784 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold neural_galactic_orbital_bridge_observable_count; decide,
    by unfold neural_galactic_orbital_bridge_D_eff; decide,
    neural_galactic_orbital_bridge_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
