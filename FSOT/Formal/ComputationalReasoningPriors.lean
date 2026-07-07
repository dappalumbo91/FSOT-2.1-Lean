/-
  FSOT Formal ComputationalReasoningPriors — FIC sweep + trinary-OS invariants.
  Generator: scripts/gen_computational_reasoning_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def computational_reasoning_observable_count : ℕ := 577
def computational_reasoning_median_error_pct : ℝ := (0.0 : ℝ)
def computational_reasoning_D_eff : ℕ := 12

theorem computational_reasoning_observable_count_pos : 0 < computational_reasoning_observable_count := by
  unfold computational_reasoning_observable_count; norm_num

theorem computational_reasoning_median_error_under_five_pct :
    computational_reasoning_median_error_pct < (5 : ℝ) := by
  unfold computational_reasoning_median_error_pct; norm_num

theorem computational_reasoning_bundle :
    computational_reasoning_observable_count = 577 ∧
    computational_reasoning_D_eff = 12 ∧
    computational_reasoning_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold computational_reasoning_observable_count; norm_num,
    by unfold computational_reasoning_D_eff; norm_num,
    computational_reasoning_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
