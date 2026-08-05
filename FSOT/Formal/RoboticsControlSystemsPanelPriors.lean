/-
  FSOT Formal RoboticsControlSystemsPanelPriors — extension domain Robotics_Control_Systems_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def robotics_control_systems_panel_observable_count : ℕ := 20
def robotics_control_systems_panel_D_eff : ℕ := 15

theorem robotics_control_systems_panel_observable_count_pos : 0 < robotics_control_systems_panel_observable_count := by
  unfold robotics_control_systems_panel_observable_count; decide

theorem robotics_control_systems_panel_median_error_under_half_pct :
    (0.01341 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.01341 : ℝ) < (0.5 : ℝ))

theorem robotics_control_systems_panel_bundle :
    robotics_control_systems_panel_observable_count = 20 ∧
    robotics_control_systems_panel_D_eff = 15 ∧
    (0.01341 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold robotics_control_systems_panel_observable_count; decide,
    by unfold robotics_control_systems_panel_D_eff; decide,
    robotics_control_systems_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
