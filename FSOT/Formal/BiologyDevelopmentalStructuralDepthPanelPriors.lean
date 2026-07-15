/-
  FSOT Formal BiologyDevelopmentalStructuralDepthPanelPriors — Tier 87 depth wave (Biology_Developmental_Structural_Depth_Panel).
  Generator: scripts/gen_tier87_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def biology_developmental_structural_depth_observable_count : ℕ := 13
def biology_developmental_structural_depth_median_error_pct : ℝ := (0.022236 : ℝ)
def biology_developmental_structural_depth_D_eff : ℕ := 17

theorem biology_developmental_structural_depth_observable_count_pos : 0 < biology_developmental_structural_depth_observable_count := by
  unfold biology_developmental_structural_depth_observable_count; norm_num

theorem biology_developmental_structural_depth_median_error_under_five_pct :
    biology_developmental_structural_depth_median_error_pct < (5 : ℝ) := by
  unfold biology_developmental_structural_depth_median_error_pct; norm_num

theorem biology_developmental_structural_depth_bundle :
    biology_developmental_structural_depth_observable_count = 13 ∧
    biology_developmental_structural_depth_D_eff = 17 ∧
    biology_developmental_structural_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold biology_developmental_structural_depth_observable_count; norm_num,
    by unfold biology_developmental_structural_depth_D_eff; norm_num,
    biology_developmental_structural_depth_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
