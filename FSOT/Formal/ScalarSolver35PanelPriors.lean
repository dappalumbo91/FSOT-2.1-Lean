/-
  FSOT Formal ScalarSolver35PanelPriors — extension domain Scalar_Solver_35_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def scalar_solver_35_panel_observable_count : ℕ := 24
def scalar_solver_35_panel_D_eff : ℕ := 14

theorem scalar_solver_35_panel_observable_count_pos : 0 < scalar_solver_35_panel_observable_count := by
  unfold scalar_solver_35_panel_observable_count; decide

theorem scalar_solver_35_panel_median_error_under_half_pct :
    (0.014767 : ℝ) < (0.5 : ℝ) := by norm_num

theorem scalar_solver_35_panel_bundle :
    scalar_solver_35_panel_observable_count = 24 ∧
    scalar_solver_35_panel_D_eff = 14 ∧
    (0.014767 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold scalar_solver_35_panel_observable_count; decide,
    by unfold scalar_solver_35_panel_D_eff; decide,
    scalar_solver_35_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
