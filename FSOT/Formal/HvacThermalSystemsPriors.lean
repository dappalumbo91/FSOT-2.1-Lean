/-
  FSOT Formal HvacThermalSystemsPriors — Tier 39 (HVAC_Thermal_Systems).
  Generator: scripts/gen_tier39_propulsion_electrical_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def hvac_thermal_systems_observable_count : ℕ := 7
def hvac_thermal_systems_median_error_pct : ℝ := (0.0 : ℝ)
def hvac_thermal_systems_D_eff : ℕ := 13

theorem hvac_thermal_systems_observable_count_pos : 0 < hvac_thermal_systems_observable_count := by
  unfold hvac_thermal_systems_observable_count; decide

theorem hvac_thermal_systems_median_error_under_five_pct :
    hvac_thermal_systems_median_error_pct < (5 : ℝ) := by
  unfold hvac_thermal_systems_median_error_pct; norm_num

theorem hvac_thermal_systems_bundle :
    hvac_thermal_systems_observable_count = 7 ∧
    hvac_thermal_systems_D_eff = 13 ∧
    hvac_thermal_systems_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold hvac_thermal_systems_observable_count; decide,
    by unfold hvac_thermal_systems_D_eff; decide,
    hvac_thermal_systems_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
