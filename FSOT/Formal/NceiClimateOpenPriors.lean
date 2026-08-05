/-
  FSOT Formal NceiClimateOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def ncei_climate_open_observable_count : ℕ := 607
def ncei_climate_open_pooled_median_error_pct : ℝ := (0.0291 : ℝ)
def ncei_climate_open_headline_median_error_pct : ℝ := (0.0291 : ℝ)
def ncei_climate_open_D_eff : ℕ := 14

theorem ncei_climate_open_observable_count_pos : 0 < ncei_climate_open_observable_count := by
  unfold ncei_climate_open_observable_count; decide

theorem ncei_climate_open_pooled_median_under_half_pct :
    ncei_climate_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold ncei_climate_open_pooled_median_error_pct
  exact (by norm_num : (0.0291  : ℝ) < 0.5)

theorem ncei_climate_open_headline_median_under_half_pct :
    ncei_climate_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold ncei_climate_open_headline_median_error_pct
  exact (by norm_num : (0.0291  : ℝ) < 0.5)

theorem ncei_climate_open_bundle :
    ncei_climate_open_observable_count = 607 ∧
    ncei_climate_open_D_eff = 14 ∧
    ncei_climate_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold ncei_climate_open_observable_count; decide
  · unfold ncei_climate_open_D_eff; decide
  · exact ncei_climate_open_pooled_median_under_half_pct

end
