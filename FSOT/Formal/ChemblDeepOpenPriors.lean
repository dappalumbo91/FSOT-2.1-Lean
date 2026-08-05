/-
  FSOT Formal ChemblDeepOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def chembl_deep_open_observable_count : ℕ := 188
def chembl_deep_open_pooled_median_error_pct : ℝ := (0.040788 : ℝ)
def chembl_deep_open_headline_median_error_pct : ℝ := (0.040788 : ℝ)
def chembl_deep_open_D_eff : ℕ := 14

theorem chembl_deep_open_observable_count_pos : 0 < chembl_deep_open_observable_count := by
  unfold chembl_deep_open_observable_count; norm_num

theorem chembl_deep_open_pooled_median_under_half_pct :
    chembl_deep_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold chembl_deep_open_pooled_median_error_pct; norm_num

theorem chembl_deep_open_headline_median_under_half_pct :
    chembl_deep_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold chembl_deep_open_headline_median_error_pct; norm_num

theorem chembl_deep_open_bundle :
    chembl_deep_open_observable_count = 188 ∧
    chembl_deep_open_D_eff = 14 ∧
    chembl_deep_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold chembl_deep_open_observable_count; norm_num
  · unfold chembl_deep_open_D_eff; norm_num
  · exact chembl_deep_open_pooled_median_under_half_pct

end
