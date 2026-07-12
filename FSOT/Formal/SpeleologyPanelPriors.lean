/-
  FSOT Formal SpeleologyPanelPriors — Tier 85 scientific expansion (Speleology_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def speleology_panel_observable_count : ℕ := 10
def speleology_panel_median_error_pct : ℝ := (0.04459 : ℝ)
def speleology_panel_D_eff : ℕ := 16

theorem speleology_panel_observable_count_pos : 0 < speleology_panel_observable_count := by
  unfold speleology_panel_observable_count; norm_num

theorem speleology_panel_median_error_under_five_pct :
    speleology_panel_median_error_pct < (5 : ℝ) := by
  unfold speleology_panel_median_error_pct; norm_num

theorem speleology_panel_bundle :
    speleology_panel_observable_count = 10 ∧
    speleology_panel_D_eff = 16 ∧
    speleology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold speleology_panel_observable_count; norm_num,
    by unfold speleology_panel_D_eff; norm_num,
    speleology_panel_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
