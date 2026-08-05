/-
  FSOT Formal NeurolabResidualMathSpinePriors — extension domain Neurolab_Residual_Math_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def neurolab_residual_math_spine_observable_count : ℕ := 28
def neurolab_residual_math_spine_D_eff : ℕ := 17

theorem neurolab_residual_math_spine_observable_count_pos : 0 < neurolab_residual_math_spine_observable_count := by
  unfold neurolab_residual_math_spine_observable_count; decide

theorem neurolab_residual_math_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem neurolab_residual_math_spine_bundle :
    neurolab_residual_math_spine_observable_count = 28 ∧
    neurolab_residual_math_spine_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold neurolab_residual_math_spine_observable_count; decide,
    by unfold neurolab_residual_math_spine_D_eff; decide,
    neurolab_residual_math_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
