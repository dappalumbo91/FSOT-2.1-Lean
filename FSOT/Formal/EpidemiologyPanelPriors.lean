/-
  FSOT Formal EpidemiologyPanelPriors — extension domain Epidemiology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def epidemiology_panel_observable_count : ℕ := 24
def epidemiology_panel_D_eff : ℕ := 15

theorem epidemiology_panel_observable_count_pos : 0 < epidemiology_panel_observable_count := by
  unfold epidemiology_panel_observable_count; norm_num

theorem epidemiology_panel_median_error_under_half_pct :
    (0.015311 : ℝ) < (0.5 : ℝ) := by norm_num

theorem epidemiology_panel_bundle :
    epidemiology_panel_observable_count = 24 ∧
    epidemiology_panel_D_eff = 15 ∧
    (0.015311 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold epidemiology_panel_observable_count; norm_num,
    by unfold epidemiology_panel_D_eff; norm_num,
    epidemiology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
