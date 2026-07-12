/-
  FSOT Formal ExogeologyPanelPriors — Tier 85 scientific expansion (Exogeology_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def exogeology_panel_observable_count : ℕ := 60
def exogeology_panel_median_error_pct : ℝ := (0.026472 : ℝ)
def exogeology_panel_D_eff : ℕ := 20

theorem exogeology_panel_observable_count_pos : 0 < exogeology_panel_observable_count := by
  unfold exogeology_panel_observable_count; norm_num

theorem exogeology_panel_median_error_under_five_pct :
    exogeology_panel_median_error_pct < (5 : ℝ) := by
  unfold exogeology_panel_median_error_pct; norm_num

theorem exogeology_panel_bundle :
    exogeology_panel_observable_count = 60 ∧
    exogeology_panel_D_eff = 20 ∧
    exogeology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold exogeology_panel_observable_count; norm_num,
    by unfold exogeology_panel_D_eff; norm_num,
    exogeology_panel_median_error_under_five_pct,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
