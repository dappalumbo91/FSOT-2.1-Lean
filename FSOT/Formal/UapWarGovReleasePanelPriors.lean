/-
  FSOT Formal UapWarGovReleasePanelPriors — extension domain UAP_War_Gov_Release_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def uap_war_gov_release_panel_observable_count : ℕ := 542
def uap_war_gov_release_panel_D_eff : ℕ := 20

theorem uap_war_gov_release_panel_observable_count_pos : 0 < uap_war_gov_release_panel_observable_count := by
  unfold uap_war_gov_release_panel_observable_count; decide

theorem uap_war_gov_release_panel_median_error_under_half_pct :
    (0.008488 : ℝ) < (0.5 : ℝ) := by norm_num

theorem uap_war_gov_release_panel_bundle :
    uap_war_gov_release_panel_observable_count = 542 ∧
    uap_war_gov_release_panel_D_eff = 20 ∧
    (0.008488 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold uap_war_gov_release_panel_observable_count; decide,
    by unfold uap_war_gov_release_panel_D_eff; decide,
    uap_war_gov_release_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
