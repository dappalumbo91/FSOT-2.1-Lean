/-
  FSOT Formal MarineBiologyPanelPriors — Tier 84 scientific expansion (Marine_Biology_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def marine_biology_panel_observable_count : ℕ := 60
def marine_biology_panel_median_error_pct : ℝ := (0.006006 : ℝ)
def marine_biology_panel_D_eff : ℕ := 17

theorem marine_biology_panel_observable_count_pos : 0 < marine_biology_panel_observable_count := by
  unfold marine_biology_panel_observable_count; norm_num

theorem marine_biology_panel_median_error_under_five_pct :
    marine_biology_panel_median_error_pct < (5 : ℝ) := by
  unfold marine_biology_panel_median_error_pct; norm_num

theorem marine_biology_panel_bundle :
    marine_biology_panel_observable_count = 60 ∧
    marine_biology_panel_D_eff = 17 ∧
    marine_biology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold marine_biology_panel_observable_count; norm_num,
    by unfold marine_biology_panel_D_eff; norm_num,
    marine_biology_panel_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
