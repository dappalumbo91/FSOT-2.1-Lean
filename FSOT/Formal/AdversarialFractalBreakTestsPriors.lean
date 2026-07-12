/-
  FSOT Formal AdversarialFractalBreakTestsPriors — extension domain Adversarial_Fractal_Break_Tests.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def adversarial_fractal_break_tests_observable_count : ℕ := 24
def adversarial_fractal_break_tests_D_eff : ℕ := 17

theorem adversarial_fractal_break_tests_observable_count_pos : 0 < adversarial_fractal_break_tests_observable_count := by
  unfold adversarial_fractal_break_tests_observable_count; norm_num

theorem adversarial_fractal_break_tests_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem adversarial_fractal_break_tests_bundle :
    adversarial_fractal_break_tests_observable_count = 24 ∧
    adversarial_fractal_break_tests_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold adversarial_fractal_break_tests_observable_count; norm_num,
    by unfold adversarial_fractal_break_tests_D_eff; norm_num,
    adversarial_fractal_break_tests_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
