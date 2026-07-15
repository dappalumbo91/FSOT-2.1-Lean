/-
  FSOT Formal VlAgentDistillPanelPriors — Tier 88 application wiring (VL_Agent_Distill_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def vl_agent_observable_count : ℕ := 6
def vl_agent_median_error_pct : ℝ := (0.031506 : ℝ)
def vl_agent_D_eff : ℕ := 14

theorem vl_agent_observable_count_pos : 0 < vl_agent_observable_count := by
  unfold vl_agent_observable_count; norm_num

theorem vl_agent_median_error_under_five_pct :
    vl_agent_median_error_pct < (5 : ℝ) := by
  unfold vl_agent_median_error_pct; norm_num

theorem vl_agent_bundle :
    vl_agent_observable_count = 6 ∧
    vl_agent_D_eff = 14 ∧
    vl_agent_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "ai") > 0 := by
  refine ⟨
    by unfold vl_agent_observable_count; norm_num,
    by unfold vl_agent_D_eff; norm_num,
    vl_agent_median_error_under_five_pct,
    ai_raw_S_positive
  ⟩

end

end FSOT.Formal
