/-
  FSOT Formal IntrinsicLlmValidatorsPanelPriors — Tier 88 application wiring (Intrinsic_LLM_Validators_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def validators_intrinsic_llm_observable_count : ℕ := 21
def validators_intrinsic_llm_median_error_pct : ℝ := (0.014767 : ℝ)
def validators_intrinsic_llm_D_eff : ℕ := 14

theorem validators_intrinsic_llm_observable_count_pos : 0 < validators_intrinsic_llm_observable_count := by
  unfold validators_intrinsic_llm_observable_count; norm_num

theorem validators_intrinsic_llm_median_error_under_five_pct :
    validators_intrinsic_llm_median_error_pct < (5 : ℝ) := by
  unfold validators_intrinsic_llm_median_error_pct; norm_num

theorem validators_intrinsic_llm_bundle :
    validators_intrinsic_llm_observable_count = 21 ∧
    validators_intrinsic_llm_D_eff = 14 ∧
    validators_intrinsic_llm_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "ai") > 0 := by
  refine ⟨
    by unfold validators_intrinsic_llm_observable_count; norm_num,
    by unfold validators_intrinsic_llm_D_eff; norm_num,
    validators_intrinsic_llm_median_error_under_five_pct,
    ai_raw_S_positive
  ⟩

end

end FSOT.Formal
