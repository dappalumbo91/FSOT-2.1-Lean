/-
  FSOT Formal EntomologyPanelPriors — Tier 84 scientific expansion (Entomology_Panel).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def entomology_panel_observable_count : ℕ := 60
def entomology_panel_median_error_pct : ℝ := (0.006006 : ℝ)
def entomology_panel_D_eff : ℕ := 16

theorem entomology_panel_observable_count_pos : 0 < entomology_panel_observable_count := by
  unfold entomology_panel_observable_count; norm_num

theorem entomology_panel_median_error_under_five_pct :
    entomology_panel_median_error_pct < (5 : ℝ) := by
  unfold entomology_panel_median_error_pct; norm_num

theorem entomology_panel_bundle :
    entomology_panel_observable_count = 60 ∧
    entomology_panel_D_eff = 16 ∧
    entomology_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold entomology_panel_observable_count; norm_num,
    by unfold entomology_panel_D_eff; norm_num,
    entomology_panel_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
