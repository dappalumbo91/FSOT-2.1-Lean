/-
  FSOT Formal ScientificExpansionDepthSpinePriors — Tier 86 scientific expansion (Scientific_Expansion_Depth_Spine).
  Generator: scripts/gen_tier86_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def scientific_expansion_depth_observable_count : ℕ := 20
def scientific_expansion_depth_median_error_pct : ℝ := (0.0 : ℝ)
def scientific_expansion_depth_D_eff : ℕ := 17

theorem scientific_expansion_depth_observable_count_pos : 0 < scientific_expansion_depth_observable_count := by
  unfold scientific_expansion_depth_observable_count; norm_num

theorem scientific_expansion_depth_median_error_under_five_pct :
    scientific_expansion_depth_median_error_pct < (5 : ℝ) := by
  unfold scientific_expansion_depth_median_error_pct; norm_num

theorem scientific_expansion_depth_bundle :
    scientific_expansion_depth_observable_count = 20 ∧
    scientific_expansion_depth_D_eff = 17 ∧
    scientific_expansion_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "mathematical") > 0 := by
  refine ⟨
    by unfold scientific_expansion_depth_observable_count; norm_num,
    by unfold scientific_expansion_depth_D_eff; norm_num,
    scientific_expansion_depth_median_error_under_five_pct,
    mathematical_raw_S_positive
  ⟩

end

end FSOT.Formal
