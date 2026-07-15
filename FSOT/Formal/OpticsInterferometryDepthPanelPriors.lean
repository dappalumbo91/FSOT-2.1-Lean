/-
  FSOT Formal OpticsInterferometryDepthPanelPriors — Tier 87 depth wave (Optics_Interferometry_Depth_Panel).
  Generator: scripts/gen_tier87_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def optics_interferometry_depth_observable_count : ℕ := 82
def optics_interferometry_depth_median_error_pct : ℝ := (0.026954 : ℝ)
def optics_interferometry_depth_D_eff : ℕ := 17

theorem optics_interferometry_depth_observable_count_pos : 0 < optics_interferometry_depth_observable_count := by
  unfold optics_interferometry_depth_observable_count; norm_num

theorem optics_interferometry_depth_median_error_under_five_pct :
    optics_interferometry_depth_median_error_pct < (5 : ℝ) := by
  unfold optics_interferometry_depth_median_error_pct; norm_num

theorem optics_interferometry_depth_bundle :
    optics_interferometry_depth_observable_count = 82 ∧
    optics_interferometry_depth_D_eff = 17 ∧
    optics_interferometry_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold optics_interferometry_depth_observable_count; norm_num,
    by unfold optics_interferometry_depth_D_eff; norm_num,
    optics_interferometry_depth_median_error_under_five_pct,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
