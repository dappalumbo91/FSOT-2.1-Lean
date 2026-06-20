/-
  FSOT Formal MathGeneratorPriors — cross-domain formula generator certificates.

  Source: Math generator/Unified/ada_spark_formula_generator/generated_formula_comparison_report.json
  Generator: scripts/gen_math_generator_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def math_generator_comparison_count : ℕ := 7
def math_generator_max_error_pct : ℝ := (1.1862232544535427 : ℝ)
def math_generator_c_eff : ℝ := (0.9577022026205612 : ℝ)
def math_generator_p_base : ℝ := (0.21234577623937845 : ℝ)

theorem math_generator_comparison_count_pos : 0 < math_generator_comparison_count := by
  unfold math_generator_comparison_count; norm_num

theorem math_generator_max_error_pct_positive : (0 : ℝ) < math_generator_max_error_pct := by
  unfold math_generator_max_error_pct; norm_num

/-- Bundle: Ada/Spark formula comparisons with particle-domain sign proxy. -/
theorem math_generator_priors_bundle :
    math_generator_comparison_count = 7 ∧
    math_generator_max_error_pct = (1.1862232544535427 : ℝ) ∧
    math_generator_c_eff = (0.9577022026205612 : ℝ) ∧
    math_generator_p_base = (0.21234577623937845 : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "particle") := by
  refine ⟨
    by unfold math_generator_comparison_count; norm_num,
    by unfold math_generator_max_error_pct; norm_num,
    by unfold math_generator_c_eff; norm_num,
    by unfold math_generator_p_base; norm_num,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
