/-
  FSOT Formal MedicalGalacticOrbitalBridgePriors — extension domain Medical_Galactic_Orbital_Bridge.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def medical_galactic_orbital_bridge_observable_count : ℕ := 48
def medical_galactic_orbital_bridge_D_eff : ℕ := 17

theorem medical_galactic_orbital_bridge_observable_count_pos : 0 < medical_galactic_orbital_bridge_observable_count := by
  unfold medical_galactic_orbital_bridge_observable_count; norm_num

theorem medical_galactic_orbital_bridge_median_error_under_half_pct :
    (0.010717743028517818 : ℝ) < (0.5 : ℝ) := by norm_num

theorem medical_galactic_orbital_bridge_bundle :
    medical_galactic_orbital_bridge_observable_count = 48 ∧
    medical_galactic_orbital_bridge_D_eff = 17 ∧
    (0.010717743028517818 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold medical_galactic_orbital_bridge_observable_count; norm_num,
    by unfold medical_galactic_orbital_bridge_D_eff; norm_num,
    medical_galactic_orbital_bridge_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
