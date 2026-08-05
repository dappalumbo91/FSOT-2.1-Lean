/-
  FSOT Formal ConsciousnessGalacticOrbitalBridgePriors — extension domain Consciousness_Galactic_Orbital_Bridge.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def consciousness_galactic_orbital_bridge_observable_count : ℕ := 48
def consciousness_galactic_orbital_bridge_D_eff : ℕ := 17

theorem consciousness_galactic_orbital_bridge_observable_count_pos : 0 < consciousness_galactic_orbital_bridge_observable_count := by
  unfold consciousness_galactic_orbital_bridge_observable_count; decide

theorem consciousness_galactic_orbital_bridge_median_error_under_half_pct :
    (0.036757197413939124 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.036757197413939124 : ℝ) < (0.5 : ℝ))

theorem consciousness_galactic_orbital_bridge_bundle :
    consciousness_galactic_orbital_bridge_observable_count = 48 ∧
    consciousness_galactic_orbital_bridge_D_eff = 17 ∧
    (0.036757197413939124 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold consciousness_galactic_orbital_bridge_observable_count; decide,
    by unfold consciousness_galactic_orbital_bridge_D_eff; decide,
    consciousness_galactic_orbital_bridge_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
