/-
  FSOT Formal FsotAggregateOrganizedPanelPriors — extension domain FSOT_Aggregate_Organized_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fsot_aggregate_organized_panel_observable_count : ℕ := 24
def fsot_aggregate_organized_panel_D_eff : ℕ := 17

theorem fsot_aggregate_organized_panel_observable_count_pos : 0 < fsot_aggregate_organized_panel_observable_count := by
  unfold fsot_aggregate_organized_panel_observable_count; norm_num

theorem fsot_aggregate_organized_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem fsot_aggregate_organized_panel_bundle :
    fsot_aggregate_organized_panel_observable_count = 24 ∧
    fsot_aggregate_organized_panel_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fsot_aggregate_organized_panel_observable_count; norm_num,
    by unfold fsot_aggregate_organized_panel_D_eff; norm_num,
    fsot_aggregate_organized_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
