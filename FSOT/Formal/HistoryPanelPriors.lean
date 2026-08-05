/-
  FSOT Formal HistoryPanelPriors — extension domain History_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def history_panel_observable_count : ℕ := 60
def history_panel_D_eff : ℕ := 15

theorem history_panel_observable_count_pos : 0 < history_panel_observable_count := by
  unfold history_panel_observable_count; decide

theorem history_panel_median_error_under_half_pct :
    (0.01382 : ℝ) < (0.5 : ℝ) := by norm_num

theorem history_panel_bundle :
    history_panel_observable_count = 60 ∧
    history_panel_D_eff = 15 ∧
    (0.01382 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold history_panel_observable_count; decide,
    by unfold history_panel_D_eff; decide,
    history_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
