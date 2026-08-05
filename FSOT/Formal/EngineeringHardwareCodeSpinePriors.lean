/-
  FSOT Formal EngineeringHardwareCodeSpinePriors — engineering/code residual panel (Engineering_Hardware_Code_Spine).
  Generator: scripts/gen_engineering_code_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def engineering_hardware_code_spine_observable_count : ℕ := 95
def engineering_hardware_code_spine_median_error_pct : ℝ := (0.0 : ℝ)
def engineering_hardware_code_spine_D_eff : ℕ := 13

theorem engineering_hardware_code_spine_observable_count_pos : 0 < engineering_hardware_code_spine_observable_count := by
  unfold engineering_hardware_code_spine_observable_count; decide

theorem engineering_hardware_code_spine_median_error_under_half_pct :
    engineering_hardware_code_spine_median_error_pct < (0.5 : ℝ) := by
  unfold engineering_hardware_code_spine_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem engineering_hardware_code_spine_bundle :
    engineering_hardware_code_spine_observable_count = 95 ∧
    engineering_hardware_code_spine_D_eff = 13 ∧
    engineering_hardware_code_spine_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold engineering_hardware_code_spine_observable_count; decide,
    by unfold engineering_hardware_code_spine_D_eff; decide,
    engineering_hardware_code_spine_median_error_under_half_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
