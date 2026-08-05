/-
  FSOT Formal OwidEpidemiologyOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def owid_epidemiology_open_observable_count : ℕ := 1778
def owid_epidemiology_open_pooled_median_error_pct : ℝ := (0.022236 : ℝ)
def owid_epidemiology_open_headline_median_error_pct : ℝ := (0.022236 : ℝ)
def owid_epidemiology_open_D_eff : ℕ := 16

theorem owid_epidemiology_open_observable_count_pos : 0 < owid_epidemiology_open_observable_count := by
  unfold owid_epidemiology_open_observable_count; norm_num

theorem owid_epidemiology_open_pooled_median_under_half_pct :
    owid_epidemiology_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold owid_epidemiology_open_pooled_median_error_pct; norm_num

theorem owid_epidemiology_open_headline_median_under_half_pct :
    owid_epidemiology_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold owid_epidemiology_open_headline_median_error_pct; norm_num

theorem owid_epidemiology_open_bundle :
    owid_epidemiology_open_observable_count = 1778 ∧
    owid_epidemiology_open_D_eff = 16 ∧
    owid_epidemiology_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold owid_epidemiology_open_observable_count; norm_num
  · unfold owid_epidemiology_open_D_eff; norm_num
  · exact owid_epidemiology_open_pooled_median_under_half_pct

end
