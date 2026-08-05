/-
  FSOT Formal ZenodoRecordsDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def zenodo_records_depth_open_observable_count : ℕ := 32
def zenodo_records_depth_open_pooled_median_error_pct : ℝ := (0.031506 : ℝ)
def zenodo_records_depth_open_headline_median_error_pct : ℝ := (0.031506 : ℝ)
def zenodo_records_depth_open_D_eff : ℕ := 12

theorem zenodo_records_depth_open_observable_count_pos : 0 < zenodo_records_depth_open_observable_count := by
  unfold zenodo_records_depth_open_observable_count; decide

theorem zenodo_records_depth_open_pooled_median_under_half_pct :
    zenodo_records_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold zenodo_records_depth_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem zenodo_records_depth_open_headline_median_under_half_pct :
    zenodo_records_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold zenodo_records_depth_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem zenodo_records_depth_open_bundle :
    zenodo_records_depth_open_observable_count = 32 ∧
    zenodo_records_depth_open_D_eff = 12 ∧
    zenodo_records_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold zenodo_records_depth_open_observable_count; decide
  · unfold zenodo_records_depth_open_D_eff; decide
  · exact zenodo_records_depth_open_pooled_median_under_half_pct

end
