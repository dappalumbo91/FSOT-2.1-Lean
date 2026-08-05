/-
  FSOT Formal CodataFullTableOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def codata_full_table_open_observable_count : ℕ := 38
def codata_full_table_open_pooled_median_error_pct : ℝ := (0.073582 : ℝ)
def codata_full_table_open_headline_median_error_pct : ℝ := (0.073582 : ℝ)
def codata_full_table_open_D_eff : ℕ := 12

theorem codata_full_table_open_observable_count_pos : 0 < codata_full_table_open_observable_count := by
  unfold codata_full_table_open_observable_count; decide

theorem codata_full_table_open_pooled_median_under_half_pct :
    codata_full_table_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold codata_full_table_open_pooled_median_error_pct
  exact (by norm_num : (0.073582  : ℝ) < 0.5)

theorem codata_full_table_open_headline_median_under_half_pct :
    codata_full_table_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold codata_full_table_open_headline_median_error_pct
  exact (by norm_num : (0.073582  : ℝ) < 0.5)

theorem codata_full_table_open_bundle :
    codata_full_table_open_observable_count = 38 ∧
    codata_full_table_open_D_eff = 12 ∧
    codata_full_table_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold codata_full_table_open_observable_count; decide
  · unfold codata_full_table_open_D_eff; decide
  · exact codata_full_table_open_pooled_median_under_half_pct

end
