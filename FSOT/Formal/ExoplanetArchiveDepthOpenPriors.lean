/-
  FSOT Formal ExoplanetArchiveDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def exoplanet_archive_depth_open_observable_count : ℕ := 1976
def exoplanet_archive_depth_open_pooled_median_error_pct : ℝ := (0.023015 : ℝ)
def exoplanet_archive_depth_open_headline_median_error_pct : ℝ := (0.023015 : ℝ)
def exoplanet_archive_depth_open_D_eff : ℕ := 16

theorem exoplanet_archive_depth_open_observable_count_pos : 0 < exoplanet_archive_depth_open_observable_count := by
  unfold exoplanet_archive_depth_open_observable_count; norm_num

theorem exoplanet_archive_depth_open_pooled_median_under_half_pct :
    exoplanet_archive_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold exoplanet_archive_depth_open_pooled_median_error_pct; norm_num

theorem exoplanet_archive_depth_open_headline_median_under_half_pct :
    exoplanet_archive_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold exoplanet_archive_depth_open_headline_median_error_pct; norm_num

theorem exoplanet_archive_depth_open_bundle :
    exoplanet_archive_depth_open_observable_count = 1976 ∧
    exoplanet_archive_depth_open_D_eff = 16 ∧
    exoplanet_archive_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold exoplanet_archive_depth_open_observable_count; norm_num
  · unfold exoplanet_archive_depth_open_D_eff; norm_num
  · exact exoplanet_archive_depth_open_pooled_median_under_half_pct

end
