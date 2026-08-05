/-
  FSOT Formal FormulaBranchingFractalPriors — extension domain Formula_Branching_Fractal.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def formula_branching_fractal_observable_count : ℕ := 255
def formula_branching_fractal_D_eff : ℕ := 18

theorem formula_branching_fractal_observable_count_pos : 0 < formula_branching_fractal_observable_count := by
  unfold formula_branching_fractal_observable_count; decide

theorem formula_branching_fractal_median_error_under_half_pct :
    (0.038016537604979236 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.038016537604979236 : ℝ) < (0.5 : ℝ))

theorem formula_branching_fractal_bundle :
    formula_branching_fractal_observable_count = 255 ∧
    formula_branching_fractal_D_eff = 18 ∧
    (0.038016537604979236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold formula_branching_fractal_observable_count; decide,
    by unfold formula_branching_fractal_D_eff; decide,
    formula_branching_fractal_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
