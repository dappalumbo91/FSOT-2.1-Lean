/-
  FSOT Formal GwoscStrainMetadataOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gwosc_strain_metadata_open_observable_count : ℕ := 54
def gwosc_strain_metadata_open_pooled_median_error_pct : ℝ := (0.008488 : ℝ)
def gwosc_strain_metadata_open_headline_median_error_pct : ℝ := (0.008488 : ℝ)
def gwosc_strain_metadata_open_D_eff : ℕ := 18

theorem gwosc_strain_metadata_open_observable_count_pos : 0 < gwosc_strain_metadata_open_observable_count := by
  unfold gwosc_strain_metadata_open_observable_count; decide

theorem gwosc_strain_metadata_open_pooled_median_under_half_pct :
    gwosc_strain_metadata_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold gwosc_strain_metadata_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem gwosc_strain_metadata_open_headline_median_under_half_pct :
    gwosc_strain_metadata_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold gwosc_strain_metadata_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem gwosc_strain_metadata_open_bundle :
    gwosc_strain_metadata_open_observable_count = 54 ∧
    gwosc_strain_metadata_open_D_eff = 18 ∧
    gwosc_strain_metadata_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold gwosc_strain_metadata_open_observable_count; decide
  · unfold gwosc_strain_metadata_open_D_eff; decide
  · exact gwosc_strain_metadata_open_pooled_median_under_half_pct

end
