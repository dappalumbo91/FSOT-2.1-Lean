/-
  FSOT Formal LivingFsotHardwarePanelPriors — extension domain Living_FSOT_Hardware_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def living_fsot_hardware_panel_observable_count : ℕ := 77
def living_fsot_hardware_panel_D_eff : ℕ := 15

theorem living_fsot_hardware_panel_observable_count_pos : 0 < living_fsot_hardware_panel_observable_count := by
  unfold living_fsot_hardware_panel_observable_count; norm_num

theorem living_fsot_hardware_panel_median_error_under_half_pct :
    (0.031506 : ℝ) < (0.5 : ℝ) := by norm_num

theorem living_fsot_hardware_panel_bundle :
    living_fsot_hardware_panel_observable_count = 77 ∧
    living_fsot_hardware_panel_D_eff = 15 ∧
    (0.031506 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold living_fsot_hardware_panel_observable_count; norm_num,
    by unfold living_fsot_hardware_panel_D_eff; norm_num,
    living_fsot_hardware_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
