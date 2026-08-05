/-
  FSOT Formal ElectricalPowerSystemsPriors — Tier 39 (Electrical_Power_Systems).
  Generator: scripts/gen_tier39_propulsion_electrical_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def electrical_power_systems_observable_count : ℕ := 9
def electrical_power_systems_median_error_pct : ℝ := (0.0 : ℝ)
def electrical_power_systems_D_eff : ℕ := 9

theorem electrical_power_systems_observable_count_pos : 0 < electrical_power_systems_observable_count := by
  unfold electrical_power_systems_observable_count; decide

theorem electrical_power_systems_median_error_under_five_pct :
    electrical_power_systems_median_error_pct < (5 : ℝ) := by
  unfold electrical_power_systems_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem electrical_power_systems_bundle :
    electrical_power_systems_observable_count = 9 ∧
    electrical_power_systems_D_eff = 9 ∧
    electrical_power_systems_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold electrical_power_systems_observable_count; decide,
    by unfold electrical_power_systems_D_eff; decide,
    electrical_power_systems_median_error_under_five_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
