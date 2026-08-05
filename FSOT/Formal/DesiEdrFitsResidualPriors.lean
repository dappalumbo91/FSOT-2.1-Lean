/-
  FSOT Formal DesiEdrFitsResidualPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def desi_edr_fits_residual_observable_count : ℕ := 97144
def desi_edr_fits_residual_pooled_median_error_pct : ℝ := (0.0224614892042 : ℝ)
def desi_edr_fits_residual_headline_median_error_pct : ℝ := (0.0224614892042 : ℝ)
def desi_edr_fits_residual_D_eff : ℕ := 18

theorem desi_edr_fits_residual_observable_count_pos : 0 < desi_edr_fits_residual_observable_count := by
  unfold desi_edr_fits_residual_observable_count; norm_num

theorem desi_edr_fits_residual_pooled_median_under_half_pct :
    desi_edr_fits_residual_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold desi_edr_fits_residual_pooled_median_error_pct; norm_num

theorem desi_edr_fits_residual_headline_median_under_half_pct :
    desi_edr_fits_residual_headline_median_error_pct < (0.5 : ℝ) := by
  unfold desi_edr_fits_residual_headline_median_error_pct; norm_num

theorem desi_edr_fits_residual_bundle :
    desi_edr_fits_residual_observable_count = 97144 ∧
    desi_edr_fits_residual_D_eff = 18 ∧
    desi_edr_fits_residual_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold desi_edr_fits_residual_observable_count; norm_num
  · unfold desi_edr_fits_residual_D_eff; norm_num
  · exact desi_edr_fits_residual_pooled_median_under_half_pct

end
