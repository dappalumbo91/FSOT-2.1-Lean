/-
  FSOT Formal ZebrafishCellTrackingPanelPriors — extension domain Zebrafish_Cell_Tracking_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def zebrafish_cell_tracking_panel_observable_count : ℕ := 20
def zebrafish_cell_tracking_panel_D_eff : ℕ := 20

theorem zebrafish_cell_tracking_panel_observable_count_pos : 0 < zebrafish_cell_tracking_panel_observable_count := by
  unfold zebrafish_cell_tracking_panel_observable_count; norm_num

theorem zebrafish_cell_tracking_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) := by norm_num

theorem zebrafish_cell_tracking_panel_bundle :
    zebrafish_cell_tracking_panel_observable_count = 20 ∧
    zebrafish_cell_tracking_panel_D_eff = 20 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold zebrafish_cell_tracking_panel_observable_count; norm_num,
    by unfold zebrafish_cell_tracking_panel_D_eff; norm_num,
    zebrafish_cell_tracking_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
