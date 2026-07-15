/-
  FSOT Formal ScalarSolver35PanelPriors — Tier 88 application wiring (Scalar_Solver_35_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def scalar_solver_observable_count : ℕ := 10
def scalar_solver_median_error_pct : ℝ := (0.014767 : ℝ)
def scalar_solver_D_eff : ℕ := 14

theorem scalar_solver_observable_count_pos : 0 < scalar_solver_observable_count := by
  unfold scalar_solver_observable_count; norm_num

theorem scalar_solver_median_error_under_five_pct :
    scalar_solver_median_error_pct < (5 : ℝ) := by
  unfold scalar_solver_median_error_pct; norm_num

theorem scalar_solver_bundle :
    scalar_solver_observable_count = 10 ∧
    scalar_solver_D_eff = 14 ∧
    scalar_solver_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "mathematical") > 0 := by
  refine ⟨
    by unfold scalar_solver_observable_count; norm_num,
    by unfold scalar_solver_D_eff; norm_num,
    scalar_solver_median_error_under_five_pct,
    mathematical_raw_S_positive
  ⟩

end

end FSOT.Formal
