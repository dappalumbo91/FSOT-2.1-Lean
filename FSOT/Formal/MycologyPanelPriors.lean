/-
  FSOT Formal MycologyPanelPriors — Tier 84 scientific expansion (Mycology_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def mycology_panel_observable_count : ℕ := 60
def mycology_panel_median_error_pct : ℝ := (0.006006 : ℝ)
def mycology_panel_D_eff : ℕ := 15

theorem mycology_panel_observable_count_pos : 0 < mycology_panel_observable_count := by
  unfold mycology_panel_observable_count; norm_num

theorem mycology_panel_median_error_under_five_pct :
    mycology_panel_median_error_pct < (5 : ℝ) := by
  unfold mycology_panel_median_error_pct; norm_num

theorem mycology_panel_bundle :
    mycology_panel_observable_count = 60 ∧
    mycology_panel_D_eff = 15 ∧
    mycology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold mycology_panel_observable_count; norm_num,
    by unfold mycology_panel_D_eff; norm_num,
    mycology_panel_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
