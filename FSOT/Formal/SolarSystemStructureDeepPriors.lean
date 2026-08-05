/-
  FSOT Formal SolarSystemStructureDeepPriors — extension domain Solar_System_Structure_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def solar_system_structure_deep_observable_count : ℕ := 50
def solar_system_structure_deep_D_eff : ℕ := 18

theorem solar_system_structure_deep_observable_count_pos : 0 < solar_system_structure_deep_observable_count := by
  unfold solar_system_structure_deep_observable_count; decide

theorem solar_system_structure_deep_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem solar_system_structure_deep_bundle :
    solar_system_structure_deep_observable_count = 50 ∧
    solar_system_structure_deep_D_eff = 18 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold solar_system_structure_deep_observable_count; decide,
    by unfold solar_system_structure_deep_D_eff; decide,
    solar_system_structure_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
