/-
  FSOT Formal CertifiedAgentQwenPriors — Qwen certified formal agent crosswalk.
  Generator: scripts/gen_certified_agent_qwen_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def certified_agent_qwen_observable_count : ℕ := 8
def certified_agent_qwen_median_error_pct : ℝ := (0.0 : ℝ)
def certified_agent_qwen_D_eff : ℕ := 12

theorem certified_agent_qwen_observable_count_pos : 0 < certified_agent_qwen_observable_count := by
  unfold certified_agent_qwen_observable_count; norm_num

theorem certified_agent_qwen_median_error_under_half_pct :
    certified_agent_qwen_median_error_pct < (0.5 : ℝ) := by
  unfold certified_agent_qwen_median_error_pct; norm_num

theorem certified_agent_qwen_bundle :
    certified_agent_qwen_observable_count = 8 ∧
    certified_agent_qwen_D_eff = 12 ∧
    certified_agent_qwen_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold certified_agent_qwen_observable_count; norm_num,
    by unfold certified_agent_qwen_D_eff; norm_num,
    certified_agent_qwen_median_error_under_half_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
