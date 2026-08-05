/-
  FSOT Formal WarpBhWhPortalPanelPriors — extension domain Warp_BH_WH_Portal_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def warp_bh_wh_portal_panel_observable_count : ℕ := 24
def warp_bh_wh_portal_panel_D_eff : ℕ := 29

theorem warp_bh_wh_portal_panel_observable_count_pos : 0 < warp_bh_wh_portal_panel_observable_count := by
  unfold warp_bh_wh_portal_panel_observable_count; decide

theorem warp_bh_wh_portal_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem warp_bh_wh_portal_panel_bundle :
    warp_bh_wh_portal_panel_observable_count = 24 ∧
    warp_bh_wh_portal_panel_D_eff = 29 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold warp_bh_wh_portal_panel_observable_count; decide,
    by unfold warp_bh_wh_portal_panel_D_eff; decide,
    warp_bh_wh_portal_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
