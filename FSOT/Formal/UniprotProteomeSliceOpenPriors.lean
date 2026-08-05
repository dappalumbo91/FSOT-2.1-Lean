/-
  FSOT Formal UniprotProteomeSliceOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def uniprot_proteome_slice_open_observable_count : ℕ := 68
def uniprot_proteome_slice_open_pooled_median_error_pct : ℝ := (0.022236 : ℝ)
def uniprot_proteome_slice_open_headline_median_error_pct : ℝ := (0.022236 : ℝ)
def uniprot_proteome_slice_open_D_eff : ℕ := 14

theorem uniprot_proteome_slice_open_observable_count_pos : 0 < uniprot_proteome_slice_open_observable_count := by
  unfold uniprot_proteome_slice_open_observable_count; decide

theorem uniprot_proteome_slice_open_pooled_median_under_half_pct :
    uniprot_proteome_slice_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold uniprot_proteome_slice_open_pooled_median_error_pct
  exact (by norm_num : (0.022236  : ℝ) < 0.5)

theorem uniprot_proteome_slice_open_headline_median_under_half_pct :
    uniprot_proteome_slice_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold uniprot_proteome_slice_open_headline_median_error_pct
  exact (by norm_num : (0.022236  : ℝ) < 0.5)

theorem uniprot_proteome_slice_open_bundle :
    uniprot_proteome_slice_open_observable_count = 68 ∧
    uniprot_proteome_slice_open_D_eff = 14 ∧
    uniprot_proteome_slice_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold uniprot_proteome_slice_open_observable_count; decide
  · unfold uniprot_proteome_slice_open_D_eff; decide
  · exact uniprot_proteome_slice_open_pooled_median_under_half_pct

end
