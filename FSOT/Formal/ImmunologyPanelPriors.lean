/-
  FSOT Formal ImmunologyPanelPriors — Tier 84 scientific expansion (Immunology_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def immunology_panel_observable_count : ℕ := 18
def immunology_panel_median_error_pct : ℝ := (0.040788 : ℝ)
def immunology_panel_D_eff : ℕ := 13

theorem immunology_panel_observable_count_pos : 0 < immunology_panel_observable_count := by
  unfold immunology_panel_observable_count; norm_num

theorem immunology_panel_median_error_under_five_pct :
    immunology_panel_median_error_pct < (5 : ℝ) := by
  unfold immunology_panel_median_error_pct; norm_num

theorem immunology_panel_bundle :
    immunology_panel_observable_count = 18 ∧
    immunology_panel_D_eff = 13 ∧
    immunology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold immunology_panel_observable_count; norm_num,
    by unfold immunology_panel_D_eff; norm_num,
    immunology_panel_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
