/-
  FSOT Formal EngineeringHardwareCodeSpinePriors — engineering/code residual panel (Engineering_Hardware_Code_Spine).
  Generator: scripts/gen_engineering_code_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def engineering_hardware_code_spine_observable_count : ℕ := 72
def engineering_hardware_code_spine_median_error_pct : ℝ := (0.0 : ℝ)
def engineering_hardware_code_spine_D_eff : ℕ := 13

theorem engineering_hardware_code_spine_observable_count_pos : 0 < engineering_hardware_code_spine_observable_count := by
  unfold engineering_hardware_code_spine_observable_count; norm_num

theorem engineering_hardware_code_spine_median_error_under_half_pct :
    engineering_hardware_code_spine_median_error_pct < (0.5 : ℝ) := by
  unfold engineering_hardware_code_spine_median_error_pct; norm_num

theorem engineering_hardware_code_spine_bundle :
    engineering_hardware_code_spine_observable_count = 72 ∧
    engineering_hardware_code_spine_D_eff = 13 ∧
    engineering_hardware_code_spine_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold engineering_hardware_code_spine_observable_count; norm_num,
    by unfold engineering_hardware_code_spine_D_eff; norm_num,
    engineering_hardware_code_spine_median_error_under_half_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
