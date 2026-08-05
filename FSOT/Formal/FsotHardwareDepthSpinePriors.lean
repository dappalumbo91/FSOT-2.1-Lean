/-
  FSOT Formal FsotHardwareDepthSpinePriors — hardware depth (FSOT_Hardware_Depth_Spine).
  Generator: scripts/gen_hardware_depth_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_hardware_depth_spine_observable_count : ℕ := 177
def fsot_hardware_depth_spine_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_hardware_depth_spine_D_eff : ℕ := 13

theorem fsot_hardware_depth_spine_observable_count_pos : 0 < fsot_hardware_depth_spine_observable_count := by
  unfold fsot_hardware_depth_spine_observable_count; decide

theorem fsot_hardware_depth_spine_median_error_under_half_pct :
    fsot_hardware_depth_spine_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_hardware_depth_spine_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem fsot_hardware_depth_spine_bundle :
    fsot_hardware_depth_spine_observable_count = 177 ∧
    fsot_hardware_depth_spine_D_eff = 13 ∧
    fsot_hardware_depth_spine_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fsot_hardware_depth_spine_observable_count; decide,
    by unfold fsot_hardware_depth_spine_D_eff; decide,
    fsot_hardware_depth_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
