/-
  FSOT Formal CardiologyPanelPriors — Tier 84 scientific expansion (Cardiology_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def cardiology_panel_observable_count : ℕ := 20
def cardiology_panel_median_error_pct : ℝ := (0.015311 : ℝ)
def cardiology_panel_D_eff : ℕ := 14

theorem cardiology_panel_observable_count_pos : 0 < cardiology_panel_observable_count := by
  unfold cardiology_panel_observable_count; norm_num

theorem cardiology_panel_median_error_under_five_pct :
    cardiology_panel_median_error_pct < (5 : ℝ) := by
  unfold cardiology_panel_median_error_pct; norm_num

theorem cardiology_panel_bundle :
    cardiology_panel_observable_count = 20 ∧
    cardiology_panel_D_eff = 14 ∧
    cardiology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold cardiology_panel_observable_count; norm_num,
    by unfold cardiology_panel_D_eff; norm_num,
    cardiology_panel_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
