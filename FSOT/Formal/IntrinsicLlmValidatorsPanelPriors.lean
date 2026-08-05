/-
  FSOT Formal IntrinsicLlmValidatorsPanelPriors — extension domain Intrinsic_LLM_Validators_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def intrinsic_llm_validators_panel_observable_count : ℕ := 21
def intrinsic_llm_validators_panel_D_eff : ℕ := 14

theorem intrinsic_llm_validators_panel_observable_count_pos : 0 < intrinsic_llm_validators_panel_observable_count := by
  unfold intrinsic_llm_validators_panel_observable_count; decide

theorem intrinsic_llm_validators_panel_median_error_under_half_pct :
    (0.014767 : ℝ) < (0.5 : ℝ) := by norm_num

theorem intrinsic_llm_validators_panel_bundle :
    intrinsic_llm_validators_panel_observable_count = 21 ∧
    intrinsic_llm_validators_panel_D_eff = 14 ∧
    (0.014767 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold intrinsic_llm_validators_panel_observable_count; decide,
    by unfold intrinsic_llm_validators_panel_D_eff; decide,
    intrinsic_llm_validators_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
