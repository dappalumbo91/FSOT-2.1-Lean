/-
  FSOT Formal OpenneuroDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def openneuro_depth_open_observable_count : ℕ := 47
def openneuro_depth_open_pooled_median_error_pct : ℝ := (0.018003 : ℝ)
def openneuro_depth_open_headline_median_error_pct : ℝ := (0.018003 : ℝ)
def openneuro_depth_open_D_eff : ℕ := 14

theorem openneuro_depth_open_observable_count_pos : 0 < openneuro_depth_open_observable_count := by
  unfold openneuro_depth_open_observable_count; decide

theorem openneuro_depth_open_pooled_median_under_half_pct :
    openneuro_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold openneuro_depth_open_pooled_median_error_pct
  exact (by norm_num : (0.018003  : ℝ) < 0.5)

theorem openneuro_depth_open_headline_median_under_half_pct :
    openneuro_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold openneuro_depth_open_headline_median_error_pct
  exact (by norm_num : (0.018003  : ℝ) < 0.5)

theorem openneuro_depth_open_bundle :
    openneuro_depth_open_observable_count = 47 ∧
    openneuro_depth_open_D_eff = 14 ∧
    openneuro_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold openneuro_depth_open_observable_count; decide
  · unfold openneuro_depth_open_D_eff; decide
  · exact openneuro_depth_open_pooled_median_under_half_pct

end
