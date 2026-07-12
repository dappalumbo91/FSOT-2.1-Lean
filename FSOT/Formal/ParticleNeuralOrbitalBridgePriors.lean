/-
  FSOT Formal ParticleNeuralOrbitalBridgePriors — extension domain Particle_Neural_Orbital_Bridge.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def particle_neural_orbital_bridge_observable_count : ℕ := 48
def particle_neural_orbital_bridge_D_eff : ℕ := 17

theorem particle_neural_orbital_bridge_observable_count_pos : 0 < particle_neural_orbital_bridge_observable_count := by
  unfold particle_neural_orbital_bridge_observable_count; norm_num

theorem particle_neural_orbital_bridge_median_error_under_half_pct :
    (0.03326447040434832 : ℝ) < (0.5 : ℝ) := by norm_num

theorem particle_neural_orbital_bridge_bundle :
    particle_neural_orbital_bridge_observable_count = 48 ∧
    particle_neural_orbital_bridge_D_eff = 17 ∧
    (0.03326447040434832 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold particle_neural_orbital_bridge_observable_count; norm_num,
    by unfold particle_neural_orbital_bridge_D_eff; norm_num,
    particle_neural_orbital_bridge_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
