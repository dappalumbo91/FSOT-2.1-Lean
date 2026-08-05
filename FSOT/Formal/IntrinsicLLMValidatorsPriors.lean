/-
  FSOT Formal IntrinsicLLMValidatorsPriors — intrinsic LLM validator tiers.
  Generator: scripts/gen_intrinsic_llm_validators_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def intrinsic_llm_validators_observable_count : ℕ := 10
def intrinsic_llm_validators_median_error_pct : ℝ := (0.0 : ℝ)
def intrinsic_llm_validators_D_eff : ℕ := 12

theorem intrinsic_llm_validators_observable_count_pos : 0 < intrinsic_llm_validators_observable_count := by
  unfold intrinsic_llm_validators_observable_count; decide

theorem intrinsic_llm_validators_median_error_under_five_pct :
    intrinsic_llm_validators_median_error_pct < (5 : ℝ) := by
  unfold intrinsic_llm_validators_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem intrinsic_llm_validators_bundle :
    intrinsic_llm_validators_observable_count = 10 ∧
    intrinsic_llm_validators_D_eff = 12 ∧
    intrinsic_llm_validators_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold intrinsic_llm_validators_observable_count; decide,
    by unfold intrinsic_llm_validators_D_eff; decide,
    intrinsic_llm_validators_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
