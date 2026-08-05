/-
  FSOT Formal DesiPublicDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def desi_public_depth_open_observable_count : ℕ := 10
def desi_public_depth_open_pooled_median_error_pct : ℝ := (0.010049 : ℝ)
def desi_public_depth_open_headline_median_error_pct : ℝ := (0.010049 : ℝ)
def desi_public_depth_open_D_eff : ℕ := 18

theorem desi_public_depth_open_observable_count_pos : 0 < desi_public_depth_open_observable_count := by
  unfold desi_public_depth_open_observable_count; decide

theorem desi_public_depth_open_pooled_median_under_half_pct :
    desi_public_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold desi_public_depth_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem desi_public_depth_open_headline_median_under_half_pct :
    desi_public_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold desi_public_depth_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem desi_public_depth_open_bundle :
    desi_public_depth_open_observable_count = 10 ∧
    desi_public_depth_open_D_eff = 18 ∧
    desi_public_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold desi_public_depth_open_observable_count; decide
  · unfold desi_public_depth_open_D_eff; decide
  · exact desi_public_depth_open_pooled_median_under_half_pct

end
