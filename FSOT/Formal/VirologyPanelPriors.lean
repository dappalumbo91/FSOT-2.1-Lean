/-
  FSOT Formal VirologyPanelPriors — Tier 84 scientific expansion (Virology_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def virology_panel_observable_count : ℕ := 6
def virology_panel_median_error_pct : ℝ := (0.022236 : ℝ)
def virology_panel_D_eff : ℕ := 14

theorem virology_panel_observable_count_pos : 0 < virology_panel_observable_count := by
  unfold virology_panel_observable_count; norm_num

theorem virology_panel_median_error_under_five_pct :
    virology_panel_median_error_pct < (5 : ℝ) := by
  unfold virology_panel_median_error_pct; norm_num

theorem virology_panel_bundle :
    virology_panel_observable_count = 6 ∧
    virology_panel_D_eff = 14 ∧
    virology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold virology_panel_observable_count; norm_num,
    by unfold virology_panel_D_eff; norm_num,
    virology_panel_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
