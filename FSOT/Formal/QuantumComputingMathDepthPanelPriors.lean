/-
  FSOT Formal QuantumComputingMathDepthPanelPriors — Tier 87 depth wave (Quantum_Computing_Math_Depth_Panel).
  Generator: scripts/gen_tier87_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_computing_math_depth_observable_count : ℕ := 77
def quantum_computing_math_depth_median_error_pct : ℝ := (0.014767 : ℝ)
def quantum_computing_math_depth_D_eff : ℕ := 19

theorem quantum_computing_math_depth_observable_count_pos : 0 < quantum_computing_math_depth_observable_count := by
  unfold quantum_computing_math_depth_observable_count; norm_num

theorem quantum_computing_math_depth_median_error_under_five_pct :
    quantum_computing_math_depth_median_error_pct < (5 : ℝ) := by
  unfold quantum_computing_math_depth_median_error_pct; norm_num

theorem quantum_computing_math_depth_bundle :
    quantum_computing_math_depth_observable_count = 77 ∧
    quantum_computing_math_depth_D_eff = 19 ∧
    quantum_computing_math_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "ai") > 0 := by
  refine ⟨
    by unfold quantum_computing_math_depth_observable_count; norm_num,
    by unfold quantum_computing_math_depth_D_eff; norm_num,
    quantum_computing_math_depth_median_error_under_five_pct,
    ai_raw_S_positive
  ⟩

end

end FSOT.Formal
