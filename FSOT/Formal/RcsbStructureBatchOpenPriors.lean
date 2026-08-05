/-
  FSOT Formal RcsbStructureBatchOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def rcsb_structure_batch_open_observable_count : ℕ := 91
def rcsb_structure_batch_open_pooled_median_error_pct : ℝ := (0.022236 : ℝ)
def rcsb_structure_batch_open_headline_median_error_pct : ℝ := (0.022236 : ℝ)
def rcsb_structure_batch_open_D_eff : ℕ := 14

theorem rcsb_structure_batch_open_observable_count_pos : 0 < rcsb_structure_batch_open_observable_count := by
  unfold rcsb_structure_batch_open_observable_count; decide

theorem rcsb_structure_batch_open_pooled_median_under_half_pct :
    rcsb_structure_batch_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold rcsb_structure_batch_open_pooled_median_error_pct
  exact (by norm_num : (0.022236  : ℝ) < 0.5)

theorem rcsb_structure_batch_open_headline_median_under_half_pct :
    rcsb_structure_batch_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold rcsb_structure_batch_open_headline_median_error_pct
  exact (by norm_num : (0.022236  : ℝ) < 0.5)

theorem rcsb_structure_batch_open_bundle :
    rcsb_structure_batch_open_observable_count = 91 ∧
    rcsb_structure_batch_open_D_eff = 14 ∧
    rcsb_structure_batch_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold rcsb_structure_batch_open_observable_count; decide
  · unfold rcsb_structure_batch_open_D_eff; decide
  · exact rcsb_structure_batch_open_pooled_median_under_half_pct

end
