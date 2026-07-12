/-
  FSOT Formal HistoryPanelPriors — Tier 85 scientific expansion (History_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def history_panel_observable_count : ℕ := 36
def history_panel_median_error_pct : ℝ := (0.01382 : ℝ)
def history_panel_D_eff : ℕ := 15

theorem history_panel_observable_count_pos : 0 < history_panel_observable_count := by
  unfold history_panel_observable_count; norm_num

theorem history_panel_median_error_under_five_pct :
    history_panel_median_error_pct < (5 : ℝ) := by
  unfold history_panel_median_error_pct; norm_num

theorem history_panel_bundle :
    history_panel_observable_count = 36 ∧
    history_panel_D_eff = 15 ∧
    history_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold history_panel_observable_count; norm_num,
    by unfold history_panel_D_eff; norm_num,
    history_panel_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
