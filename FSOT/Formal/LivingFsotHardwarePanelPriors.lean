/-
  FSOT Formal LivingFsotHardwarePanelPriors — Tier 88 application wiring (Living_FSOT_Hardware_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def living_fsot_hardware_observable_count : ℕ := 77
def living_fsot_hardware_median_error_pct : ℝ := (0.031506 : ℝ)
def living_fsot_hardware_D_eff : ℕ := 15

theorem living_fsot_hardware_observable_count_pos : 0 < living_fsot_hardware_observable_count := by
  unfold living_fsot_hardware_observable_count; norm_num

theorem living_fsot_hardware_median_error_under_five_pct :
    living_fsot_hardware_median_error_pct < (5 : ℝ) := by
  unfold living_fsot_hardware_median_error_pct; norm_num

theorem living_fsot_hardware_bundle :
    living_fsot_hardware_observable_count = 77 ∧
    living_fsot_hardware_D_eff = 15 ∧
    living_fsot_hardware_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "neural") > 0 := by
  refine ⟨
    by unfold living_fsot_hardware_observable_count; norm_num,
    by unfold living_fsot_hardware_D_eff; norm_num,
    living_fsot_hardware_median_error_under_five_pct,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
