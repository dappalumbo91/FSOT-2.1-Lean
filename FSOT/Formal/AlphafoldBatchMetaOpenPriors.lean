/-
  FSOT Formal AlphafoldBatchMetaOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def alphafold_batch_meta_open_observable_count : ℕ := 182
def alphafold_batch_meta_open_pooled_median_error_pct : ℝ := (0.015311 : ℝ)
def alphafold_batch_meta_open_headline_median_error_pct : ℝ := (0.015311 : ℝ)
def alphafold_batch_meta_open_D_eff : ℕ := 14

theorem alphafold_batch_meta_open_observable_count_pos : 0 < alphafold_batch_meta_open_observable_count := by
  unfold alphafold_batch_meta_open_observable_count; decide

theorem alphafold_batch_meta_open_pooled_median_under_half_pct :
    alphafold_batch_meta_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold alphafold_batch_meta_open_pooled_median_error_pct
  exact (by norm_num : (0.015311  : ℝ) < 0.5)

theorem alphafold_batch_meta_open_headline_median_under_half_pct :
    alphafold_batch_meta_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold alphafold_batch_meta_open_headline_median_error_pct
  exact (by norm_num : (0.015311  : ℝ) < 0.5)

theorem alphafold_batch_meta_open_bundle :
    alphafold_batch_meta_open_observable_count = 182 ∧
    alphafold_batch_meta_open_D_eff = 14 ∧
    alphafold_batch_meta_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold alphafold_batch_meta_open_observable_count; decide
  · unfold alphafold_batch_meta_open_D_eff; decide
  · exact alphafold_batch_meta_open_pooled_median_under_half_pct

end
