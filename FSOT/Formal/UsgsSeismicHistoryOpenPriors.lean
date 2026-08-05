/-
  FSOT Formal UsgsSeismicHistoryOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def usgs_seismic_history_open_observable_count : ℕ := 398
def usgs_seismic_history_open_pooled_median_error_pct : ℝ := (0.022295 : ℝ)
def usgs_seismic_history_open_headline_median_error_pct : ℝ := (0.022295 : ℝ)
def usgs_seismic_history_open_D_eff : ℕ := 16

theorem usgs_seismic_history_open_observable_count_pos : 0 < usgs_seismic_history_open_observable_count := by
  unfold usgs_seismic_history_open_observable_count; decide

theorem usgs_seismic_history_open_pooled_median_under_half_pct :
    usgs_seismic_history_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold usgs_seismic_history_open_pooled_median_error_pct
  exact (by norm_num : (0.022295  : ℝ) < 0.5)

theorem usgs_seismic_history_open_headline_median_under_half_pct :
    usgs_seismic_history_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold usgs_seismic_history_open_headline_median_error_pct
  exact (by norm_num : (0.022295  : ℝ) < 0.5)

theorem usgs_seismic_history_open_bundle :
    usgs_seismic_history_open_observable_count = 398 ∧
    usgs_seismic_history_open_D_eff = 16 ∧
    usgs_seismic_history_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold usgs_seismic_history_open_observable_count; decide
  · unfold usgs_seismic_history_open_D_eff; decide
  · exact usgs_seismic_history_open_pooled_median_under_half_pct

end
