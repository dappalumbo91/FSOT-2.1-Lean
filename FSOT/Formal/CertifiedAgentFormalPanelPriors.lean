/-
  FSOT Formal CertifiedAgentFormalPanelPriors — Tier 88 application wiring (Certified_Agent_Formal_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def certified_agent_formal_observable_count : ℕ := 13
def certified_agent_formal_median_error_pct : ℝ := (0.014767 : ℝ)
def certified_agent_formal_D_eff : ℕ := 14

theorem certified_agent_formal_observable_count_pos : 0 < certified_agent_formal_observable_count := by
  unfold certified_agent_formal_observable_count; norm_num

theorem certified_agent_formal_median_error_under_five_pct :
    certified_agent_formal_median_error_pct < (5 : ℝ) := by
  unfold certified_agent_formal_median_error_pct; norm_num

theorem certified_agent_formal_bundle :
    certified_agent_formal_observable_count = 13 ∧
    certified_agent_formal_D_eff = 14 ∧
    certified_agent_formal_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "ai") > 0 := by
  refine ⟨
    by unfold certified_agent_formal_observable_count; norm_num,
    by unfold certified_agent_formal_D_eff; norm_num,
    certified_agent_formal_median_error_under_five_pct,
    ai_raw_S_positive
  ⟩

end

end FSOT.Formal
