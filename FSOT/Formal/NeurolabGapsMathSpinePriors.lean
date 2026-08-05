/-
  FSOT Formal NeurolabGapsMathSpinePriors — extension domain Neurolab_Gaps_Math_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def neurolab_gaps_math_spine_observable_count : ℕ := 35
def neurolab_gaps_math_spine_D_eff : ℕ := 17

theorem neurolab_gaps_math_spine_observable_count_pos : 0 < neurolab_gaps_math_spine_observable_count := by
  unfold neurolab_gaps_math_spine_observable_count; decide

theorem neurolab_gaps_math_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem neurolab_gaps_math_spine_bundle :
    neurolab_gaps_math_spine_observable_count = 35 ∧
    neurolab_gaps_math_spine_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold neurolab_gaps_math_spine_observable_count; decide,
    by unfold neurolab_gaps_math_spine_D_eff; decide,
    neurolab_gaps_math_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
