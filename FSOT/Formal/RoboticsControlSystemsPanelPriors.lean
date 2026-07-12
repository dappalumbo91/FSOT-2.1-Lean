/-
  FSOT Formal RoboticsControlSystemsPanelPriors — Tier 84 scientific expansion (Robotics_Control_Systems_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def robotics_panel_observable_count : ℕ := 20
def robotics_panel_median_error_pct : ℝ := (0.01341 : ℝ)
def robotics_panel_D_eff : ℕ := 15

theorem robotics_panel_observable_count_pos : 0 < robotics_panel_observable_count := by
  unfold robotics_panel_observable_count; norm_num

theorem robotics_panel_median_error_under_five_pct :
    robotics_panel_median_error_pct < (5 : ℝ) := by
  unfold robotics_panel_median_error_pct; norm_num

theorem robotics_panel_bundle :
    robotics_panel_observable_count = 20 ∧
    robotics_panel_D_eff = 15 ∧
    robotics_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold robotics_panel_observable_count; norm_num,
    by unfold robotics_panel_D_eff; norm_num,
    robotics_panel_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
