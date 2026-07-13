/-
  FSOT Formal ZebrafishCellTrackingPanelPriors — Tier 95 Zebrahub developmental (Zebrafish_Cell_Tracking_Panel).
  Generator: scripts/gen_tier95_zebrahub_development_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def zebrafish_cell_tracking_observable_count : ℕ := 20
def zebrafish_cell_tracking_median_error_pct : ℝ := (0.022236 : ℝ)
def zebrafish_cell_tracking_D_eff : ℕ := 20

theorem zebrafish_cell_tracking_observable_count_pos : 0 < zebrafish_cell_tracking_observable_count := by
  unfold zebrafish_cell_tracking_observable_count; norm_num

theorem zebrafish_cell_tracking_median_error_under_five_pct :
    zebrafish_cell_tracking_median_error_pct < (5 : ℝ) := by
  unfold zebrafish_cell_tracking_median_error_pct; norm_num

theorem zebrafish_cell_tracking_bundle :
    zebrafish_cell_tracking_observable_count = 20 ∧
    zebrafish_cell_tracking_D_eff = 20 ∧
    zebrafish_cell_tracking_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold zebrafish_cell_tracking_observable_count; norm_num,
    by unfold zebrafish_cell_tracking_D_eff; norm_num,
    zebrafish_cell_tracking_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
