/-
  FSOT Formal PaleoclimatePanelPriors — Tier 85 scientific expansion (Paleoclimate_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def paleoclimate_panel_observable_count : ℕ := 20
def paleoclimate_panel_median_error_pct : ℝ := (0.006006 : ℝ)
def paleoclimate_panel_D_eff : ℕ := 17

theorem paleoclimate_panel_observable_count_pos : 0 < paleoclimate_panel_observable_count := by
  unfold paleoclimate_panel_observable_count; norm_num

theorem paleoclimate_panel_median_error_under_five_pct :
    paleoclimate_panel_median_error_pct < (5 : ℝ) := by
  unfold paleoclimate_panel_median_error_pct; norm_num

theorem paleoclimate_panel_bundle :
    paleoclimate_panel_observable_count = 20 ∧
    paleoclimate_panel_D_eff = 17 ∧
    paleoclimate_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold paleoclimate_panel_observable_count; norm_num,
    by unfold paleoclimate_panel_D_eff; norm_num,
    paleoclimate_panel_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
