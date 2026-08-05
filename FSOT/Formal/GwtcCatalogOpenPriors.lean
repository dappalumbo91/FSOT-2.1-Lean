/-
  FSOT Formal GwtcCatalogOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gwtc_catalog_open_observable_count : ℕ := 1972
def gwtc_catalog_open_pooled_median_error_pct : ℝ := (0.008488 : ℝ)
def gwtc_catalog_open_headline_median_error_pct : ℝ := (0.008488 : ℝ)
def gwtc_catalog_open_D_eff : ℕ := 18

theorem gwtc_catalog_open_observable_count_pos : 0 < gwtc_catalog_open_observable_count := by
  unfold gwtc_catalog_open_observable_count; decide

theorem gwtc_catalog_open_pooled_median_under_half_pct :
    gwtc_catalog_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold gwtc_catalog_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem gwtc_catalog_open_headline_median_under_half_pct :
    gwtc_catalog_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold gwtc_catalog_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem gwtc_catalog_open_bundle :
    gwtc_catalog_open_observable_count = 1972 ∧
    gwtc_catalog_open_D_eff = 18 ∧
    gwtc_catalog_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold gwtc_catalog_open_observable_count; decide
  · unfold gwtc_catalog_open_D_eff; decide
  · exact gwtc_catalog_open_pooled_median_under_half_pct

end
