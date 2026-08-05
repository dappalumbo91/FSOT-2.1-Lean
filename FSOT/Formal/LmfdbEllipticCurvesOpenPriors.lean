/-
  FSOT Formal LmfdbEllipticCurvesOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def lmfdb_elliptic_curves_open_observable_count : ℕ := 1016
def lmfdb_elliptic_curves_open_pooled_median_error_pct : ℝ := (0.014767 : ℝ)
def lmfdb_elliptic_curves_open_headline_median_error_pct : ℝ := (0.014767 : ℝ)
def lmfdb_elliptic_curves_open_D_eff : ℕ := 14

theorem lmfdb_elliptic_curves_open_observable_count_pos : 0 < lmfdb_elliptic_curves_open_observable_count := by
  unfold lmfdb_elliptic_curves_open_observable_count; decide

theorem lmfdb_elliptic_curves_open_pooled_median_under_half_pct :
    lmfdb_elliptic_curves_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold lmfdb_elliptic_curves_open_pooled_median_error_pct
  exact (by norm_num : (0.014767  : ℝ) < 0.5)

theorem lmfdb_elliptic_curves_open_headline_median_under_half_pct :
    lmfdb_elliptic_curves_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold lmfdb_elliptic_curves_open_headline_median_error_pct
  exact (by norm_num : (0.014767  : ℝ) < 0.5)

theorem lmfdb_elliptic_curves_open_bundle :
    lmfdb_elliptic_curves_open_observable_count = 1016 ∧
    lmfdb_elliptic_curves_open_D_eff = 14 ∧
    lmfdb_elliptic_curves_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold lmfdb_elliptic_curves_open_observable_count; decide
  · unfold lmfdb_elliptic_curves_open_D_eff; decide
  · exact lmfdb_elliptic_curves_open_pooled_median_under_half_pct

end
