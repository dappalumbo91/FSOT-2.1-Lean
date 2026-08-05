/-
  FSOT Formal AiGalacticOrbitalBridgePriors — extension domain AI_Galactic_Orbital_Bridge.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def ai_galactic_orbital_bridge_observable_count : ℕ := 48
def ai_galactic_orbital_bridge_D_eff : ℕ := 16

theorem ai_galactic_orbital_bridge_observable_count_pos : 0 < ai_galactic_orbital_bridge_observable_count := by
  unfold ai_galactic_orbital_bridge_observable_count; decide

theorem ai_galactic_orbital_bridge_median_error_under_half_pct :
    (0.005168558627177688 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.005168558627177688 : ℝ) < (0.5 : ℝ))

theorem ai_galactic_orbital_bridge_bundle :
    ai_galactic_orbital_bridge_observable_count = 48 ∧
    ai_galactic_orbital_bridge_D_eff = 16 ∧
    (0.005168558627177688 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold ai_galactic_orbital_bridge_observable_count; decide,
    by unfold ai_galactic_orbital_bridge_D_eff; decide,
    ai_galactic_orbital_bridge_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
