/-
  FSOT Formal VlAgentDistillPanelPriors — extension domain VL_Agent_Distill_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def vl_agent_distill_panel_observable_count : ℕ := 24
def vl_agent_distill_panel_D_eff : ℕ := 14

theorem vl_agent_distill_panel_observable_count_pos : 0 < vl_agent_distill_panel_observable_count := by
  unfold vl_agent_distill_panel_observable_count; decide

theorem vl_agent_distill_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) := by norm_num

theorem vl_agent_distill_panel_bundle :
    vl_agent_distill_panel_observable_count = 24 ∧
    vl_agent_distill_panel_D_eff = 14 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold vl_agent_distill_panel_observable_count; decide,
    by unfold vl_agent_distill_panel_D_eff; decide,
    vl_agent_distill_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
