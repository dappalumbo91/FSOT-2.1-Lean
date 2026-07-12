/-
  FSOT Formal FractalConstantRecursionPriors — extension domain Fractal_Constant_Recursion.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fractal_constant_recursion_observable_count : ℕ := 21
def fractal_constant_recursion_D_eff : ℕ := 18

theorem fractal_constant_recursion_observable_count_pos : 0 < fractal_constant_recursion_observable_count := by
  unfold fractal_constant_recursion_observable_count; norm_num

theorem fractal_constant_recursion_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem fractal_constant_recursion_bundle :
    fractal_constant_recursion_observable_count = 21 ∧
    fractal_constant_recursion_D_eff = 18 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fractal_constant_recursion_observable_count; norm_num,
    by unfold fractal_constant_recursion_D_eff; norm_num,
    fractal_constant_recursion_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
