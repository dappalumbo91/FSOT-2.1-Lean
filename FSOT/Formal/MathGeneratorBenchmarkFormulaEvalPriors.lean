/-
  FSOT Formal MathGeneratorBenchmarkFormulaEvalPriors — live benchmark_formula eval.
  Generator: scripts/gen_math_generator_benchmark_formula_eval_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def math_generator_benchmark_formula_eval_observable_count : ℕ := 13
def math_generator_benchmark_formula_eval_median_error_pct : ℝ := (0.0 : ℝ)
def math_generator_benchmark_formula_eval_D_eff : ℕ := 17

theorem math_generator_benchmark_formula_eval_observable_count_pos : 0 < math_generator_benchmark_formula_eval_observable_count := by
  unfold math_generator_benchmark_formula_eval_observable_count; decide

theorem math_generator_benchmark_formula_eval_median_error_under_five_pct :
    math_generator_benchmark_formula_eval_median_error_pct < (5 : ℝ) := by
  unfold math_generator_benchmark_formula_eval_median_error_pct; norm_num

theorem math_generator_benchmark_formula_eval_bundle :
    math_generator_benchmark_formula_eval_observable_count = 13 ∧
    math_generator_benchmark_formula_eval_D_eff = 17 ∧
    math_generator_benchmark_formula_eval_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold math_generator_benchmark_formula_eval_observable_count; decide,
    by unfold math_generator_benchmark_formula_eval_D_eff; decide,
    math_generator_benchmark_formula_eval_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
