/-
  FSOT Formal PaleontologyPanelPriors — Tier 84 scientific expansion (Paleontology_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def paleontology_panel_observable_count : ℕ := 80
def paleontology_panel_median_error_pct : ℝ := (0.0167305 : ℝ)
def paleontology_panel_D_eff : ℕ := 18

theorem paleontology_panel_observable_count_pos : 0 < paleontology_panel_observable_count := by
  unfold paleontology_panel_observable_count; norm_num

theorem paleontology_panel_median_error_under_five_pct :
    paleontology_panel_median_error_pct < (5 : ℝ) := by
  unfold paleontology_panel_median_error_pct; norm_num

theorem paleontology_panel_bundle :
    paleontology_panel_observable_count = 80 ∧
    paleontology_panel_D_eff = 18 ∧
    paleontology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold paleontology_panel_observable_count; norm_num,
    by unfold paleontology_panel_D_eff; norm_num,
    paleontology_panel_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
