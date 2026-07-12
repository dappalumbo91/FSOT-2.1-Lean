/-
  FSOT Formal LawPolicyPanelPriors — Tier 85 scientific expansion (Law_Policy_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def law_policy_panel_observable_count : ℕ := 20
def law_policy_panel_median_error_pct : ℝ := (0.013003 : ℝ)
def law_policy_panel_D_eff : ℕ := 17

theorem law_policy_panel_observable_count_pos : 0 < law_policy_panel_observable_count := by
  unfold law_policy_panel_observable_count; norm_num

theorem law_policy_panel_median_error_under_five_pct :
    law_policy_panel_median_error_pct < (5 : ℝ) := by
  unfold law_policy_panel_median_error_pct; norm_num

theorem law_policy_panel_bundle :
    law_policy_panel_observable_count = 20 ∧
    law_policy_panel_D_eff = 17 ∧
    law_policy_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold law_policy_panel_observable_count; norm_num,
    by unfold law_policy_panel_D_eff; norm_num,
    law_policy_panel_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
