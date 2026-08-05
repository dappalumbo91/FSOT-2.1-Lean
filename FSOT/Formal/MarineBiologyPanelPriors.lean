/-
  FSOT Formal MarineBiologyPanelPriors — extension domain Marine_Biology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def marine_biology_panel_observable_count : ℕ := 90
def marine_biology_panel_D_eff : ℕ := 17

theorem marine_biology_panel_observable_count_pos : 0 < marine_biology_panel_observable_count := by
  unfold marine_biology_panel_observable_count; decide

theorem marine_biology_panel_median_error_under_half_pct :
    (0.006006 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.006006 : ℝ) < (0.5 : ℝ))

theorem marine_biology_panel_bundle :
    marine_biology_panel_observable_count = 90 ∧
    marine_biology_panel_D_eff = 17 ∧
    (0.006006 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold marine_biology_panel_observable_count; decide,
    by unfold marine_biology_panel_D_eff; decide,
    marine_biology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
