/-
  FSOT Formal GwasCatalogDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gwas_catalog_depth_open_observable_count : ℕ := 81
def gwas_catalog_depth_open_pooled_median_error_pct : ℝ := (0.022236 : ℝ)
def gwas_catalog_depth_open_headline_median_error_pct : ℝ := (0.022236 : ℝ)
def gwas_catalog_depth_open_D_eff : ℕ := 14

theorem gwas_catalog_depth_open_observable_count_pos : 0 < gwas_catalog_depth_open_observable_count := by
  unfold gwas_catalog_depth_open_observable_count; decide

theorem gwas_catalog_depth_open_pooled_median_under_half_pct :
    gwas_catalog_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold gwas_catalog_depth_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem gwas_catalog_depth_open_headline_median_under_half_pct :
    gwas_catalog_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold gwas_catalog_depth_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem gwas_catalog_depth_open_bundle :
    gwas_catalog_depth_open_observable_count = 81 ∧
    gwas_catalog_depth_open_D_eff = 14 ∧
    gwas_catalog_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold gwas_catalog_depth_open_observable_count; decide
  · unfold gwas_catalog_depth_open_D_eff; decide
  · exact gwas_catalog_depth_open_pooled_median_under_half_pct

end
