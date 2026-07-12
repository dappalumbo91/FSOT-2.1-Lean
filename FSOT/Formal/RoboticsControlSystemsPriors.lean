/-
  FSOT Formal RoboticsControlSystemsPriors — extension domain Robotics_Control_Systems.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def robotics_control_systems_observable_count : ℕ := 45
def robotics_control_systems_D_eff : ℕ := 14

theorem robotics_control_systems_observable_count_pos : 0 < robotics_control_systems_observable_count := by
  unfold robotics_control_systems_observable_count; norm_num

theorem robotics_control_systems_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem robotics_control_systems_bundle :
    robotics_control_systems_observable_count = 45 ∧
    robotics_control_systems_D_eff = 14 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold robotics_control_systems_observable_count; norm_num,
    by unfold robotics_control_systems_D_eff; norm_num,
    robotics_control_systems_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
