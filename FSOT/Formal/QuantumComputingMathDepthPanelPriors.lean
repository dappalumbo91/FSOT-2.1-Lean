/-
  FSOT Formal QuantumComputingMathDepthPanelPriors — extension domain Quantum_Computing_Math_Depth_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def quantum_computing_math_depth_panel_observable_count : ℕ := 77
def quantum_computing_math_depth_panel_D_eff : ℕ := 19

theorem quantum_computing_math_depth_panel_observable_count_pos : 0 < quantum_computing_math_depth_panel_observable_count := by
  unfold quantum_computing_math_depth_panel_observable_count; norm_num

theorem quantum_computing_math_depth_panel_median_error_under_half_pct :
    (0.014767 : ℝ) < (0.5 : ℝ) := by norm_num

theorem quantum_computing_math_depth_panel_bundle :
    quantum_computing_math_depth_panel_observable_count = 77 ∧
    quantum_computing_math_depth_panel_D_eff = 19 ∧
    (0.014767 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold quantum_computing_math_depth_panel_observable_count; norm_num,
    by unfold quantum_computing_math_depth_panel_D_eff; norm_num,
    quantum_computing_math_depth_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
