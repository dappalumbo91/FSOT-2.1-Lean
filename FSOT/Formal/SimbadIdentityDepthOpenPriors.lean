/-
  FSOT Formal SimbadIdentityDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def simbad_identity_depth_open_observable_count : ℕ := 1365
def simbad_identity_depth_open_pooled_median_error_pct : ℝ := (0.022461 : ℝ)
def simbad_identity_depth_open_headline_median_error_pct : ℝ := (0.022461 : ℝ)
def simbad_identity_depth_open_D_eff : ℕ := 16

theorem simbad_identity_depth_open_observable_count_pos : 0 < simbad_identity_depth_open_observable_count := by
  unfold simbad_identity_depth_open_observable_count; decide

theorem simbad_identity_depth_open_pooled_median_under_half_pct :
    simbad_identity_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold simbad_identity_depth_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem simbad_identity_depth_open_headline_median_under_half_pct :
    simbad_identity_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold simbad_identity_depth_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem simbad_identity_depth_open_bundle :
    simbad_identity_depth_open_observable_count = 1365 ∧
    simbad_identity_depth_open_D_eff = 16 ∧
    simbad_identity_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold simbad_identity_depth_open_observable_count; decide
  · unfold simbad_identity_depth_open_D_eff; decide
  · exact simbad_identity_depth_open_pooled_median_under_half_pct

end
