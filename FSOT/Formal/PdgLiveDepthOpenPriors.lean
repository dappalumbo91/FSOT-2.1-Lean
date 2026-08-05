/-
  FSOT Formal PdgLiveDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pdg_live_depth_open_observable_count : ℕ := 33
def pdg_live_depth_open_pooled_median_error_pct : ℝ := (0.009504 : ℝ)
def pdg_live_depth_open_headline_median_error_pct : ℝ := (0.009504 : ℝ)
def pdg_live_depth_open_D_eff : ℕ := 14

theorem pdg_live_depth_open_observable_count_pos : 0 < pdg_live_depth_open_observable_count := by
  unfold pdg_live_depth_open_observable_count; decide

theorem pdg_live_depth_open_pooled_median_under_half_pct :
    pdg_live_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold pdg_live_depth_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem pdg_live_depth_open_headline_median_under_half_pct :
    pdg_live_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold pdg_live_depth_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem pdg_live_depth_open_bundle :
    pdg_live_depth_open_observable_count = 33 ∧
    pdg_live_depth_open_D_eff = 14 ∧
    pdg_live_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold pdg_live_depth_open_observable_count; decide
  · unfold pdg_live_depth_open_D_eff; decide
  · exact pdg_live_depth_open_pooled_median_under_half_pct

end
