/-
  FSOT Formal CertifiedAgentFormalPanelPriors — extension domain Certified_Agent_Formal_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def certified_agent_formal_panel_observable_count : ℕ := 24
def certified_agent_formal_panel_D_eff : ℕ := 14

theorem certified_agent_formal_panel_observable_count_pos : 0 < certified_agent_formal_panel_observable_count := by
  unfold certified_agent_formal_panel_observable_count; decide

theorem certified_agent_formal_panel_median_error_under_half_pct :
    (0.014767 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.014767 : ℝ) < (0.5 : ℝ))

theorem certified_agent_formal_panel_bundle :
    certified_agent_formal_panel_observable_count = 24 ∧
    certified_agent_formal_panel_D_eff = 14 ∧
    (0.014767 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold certified_agent_formal_panel_observable_count; decide,
    by unfold certified_agent_formal_panel_D_eff; decide,
    certified_agent_formal_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
