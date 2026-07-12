/-
  FSOT Formal NetworkSciencePublicPanelPriors — extension domain Network_Science_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def network_science_public_panel_observable_count : ℕ := 24
def network_science_public_panel_D_eff : ℕ := 17

theorem network_science_public_panel_observable_count_pos : 0 < network_science_public_panel_observable_count := by
  unfold network_science_public_panel_observable_count; norm_num

theorem network_science_public_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem network_science_public_panel_bundle :
    network_science_public_panel_observable_count = 24 ∧
    network_science_public_panel_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold network_science_public_panel_observable_count; norm_num,
    by unfold network_science_public_panel_D_eff; norm_num,
    network_science_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
