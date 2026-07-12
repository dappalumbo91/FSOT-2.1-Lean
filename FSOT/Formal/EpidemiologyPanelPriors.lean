/-
  FSOT Formal EpidemiologyPanelPriors — Tier 84 scientific expansion (Epidemiology_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def epidemiology_panel_observable_count : ℕ := 15
def epidemiology_panel_median_error_pct : ℝ := (0.015311 : ℝ)
def epidemiology_panel_D_eff : ℕ := 15

theorem epidemiology_panel_observable_count_pos : 0 < epidemiology_panel_observable_count := by
  unfold epidemiology_panel_observable_count; norm_num

theorem epidemiology_panel_median_error_under_five_pct :
    epidemiology_panel_median_error_pct < (5 : ℝ) := by
  unfold epidemiology_panel_median_error_pct; norm_num

theorem epidemiology_panel_bundle :
    epidemiology_panel_observable_count = 15 ∧
    epidemiology_panel_D_eff = 15 ∧
    epidemiology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold epidemiology_panel_observable_count; norm_num,
    by unfold epidemiology_panel_D_eff; norm_num,
    epidemiology_panel_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
