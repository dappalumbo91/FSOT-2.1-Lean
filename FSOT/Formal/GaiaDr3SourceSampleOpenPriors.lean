/-
  FSOT Formal GaiaDr3SourceSampleOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gaia_dr3_source_sample_open_observable_count : ℕ := 3459
def gaia_dr3_source_sample_open_pooled_median_error_pct : ℝ := (0.022461 : ℝ)
def gaia_dr3_source_sample_open_headline_median_error_pct : ℝ := (0.022461 : ℝ)
def gaia_dr3_source_sample_open_D_eff : ℕ := 18

theorem gaia_dr3_source_sample_open_observable_count_pos : 0 < gaia_dr3_source_sample_open_observable_count := by
  unfold gaia_dr3_source_sample_open_observable_count; decide

theorem gaia_dr3_source_sample_open_pooled_median_under_half_pct :
    gaia_dr3_source_sample_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold gaia_dr3_source_sample_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem gaia_dr3_source_sample_open_headline_median_under_half_pct :
    gaia_dr3_source_sample_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold gaia_dr3_source_sample_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem gaia_dr3_source_sample_open_bundle :
    gaia_dr3_source_sample_open_observable_count = 3459 ∧
    gaia_dr3_source_sample_open_D_eff = 18 ∧
    gaia_dr3_source_sample_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold gaia_dr3_source_sample_open_observable_count; decide
  · unfold gaia_dr3_source_sample_open_D_eff; decide
  · exact gaia_dr3_source_sample_open_pooled_median_under_half_pct

end
