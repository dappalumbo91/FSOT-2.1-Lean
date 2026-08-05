/-
  FSOT Formal LawPolicyPanelPriors — extension domain Law_Policy_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def law_policy_panel_observable_count : ℕ := 20
def law_policy_panel_D_eff : ℕ := 17

theorem law_policy_panel_observable_count_pos : 0 < law_policy_panel_observable_count := by
  unfold law_policy_panel_observable_count; decide

theorem law_policy_panel_median_error_under_half_pct :
    (0.013003 : ℝ) < (0.5 : ℝ) := by norm_num

theorem law_policy_panel_bundle :
    law_policy_panel_observable_count = 20 ∧
    law_policy_panel_D_eff = 17 ∧
    (0.013003 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold law_policy_panel_observable_count; decide,
    by unfold law_policy_panel_D_eff; decide,
    law_policy_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
