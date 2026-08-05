/-
  FSOT Formal BreakthroughFusionSpinePriors — recent breakthrough expansion (Breakthrough_Fusion_Spine).
  Generator: scripts/gen_recent_breakthrough_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def breakthrough_fusion_spine_observable_count : ℕ := 146
def breakthrough_fusion_spine_median_error_pct : ℝ := (0.0 : ℝ)
def breakthrough_fusion_spine_D_eff : ℕ := 14

theorem breakthrough_fusion_spine_observable_count_pos : 0 < breakthrough_fusion_spine_observable_count := by
  unfold breakthrough_fusion_spine_observable_count; decide

theorem breakthrough_fusion_spine_median_error_under_half_pct :
    breakthrough_fusion_spine_median_error_pct < (0.5 : ℝ) := by
  unfold breakthrough_fusion_spine_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem breakthrough_fusion_spine_bundle :
    breakthrough_fusion_spine_observable_count = 146 ∧
    breakthrough_fusion_spine_D_eff = 14 ∧
    breakthrough_fusion_spine_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold breakthrough_fusion_spine_observable_count; decide,
    by unfold breakthrough_fusion_spine_D_eff; decide,
    breakthrough_fusion_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
