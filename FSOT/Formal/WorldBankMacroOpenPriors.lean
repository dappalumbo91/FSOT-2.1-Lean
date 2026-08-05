/-
  FSOT Formal WorldBankMacroOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def world_bank_macro_open_observable_count : ℕ := 605
def world_bank_macro_open_pooled_median_error_pct : ℝ := (0.02584 : ℝ)
def world_bank_macro_open_headline_median_error_pct : ℝ := (0.02584 : ℝ)
def world_bank_macro_open_D_eff : ℕ := 18

theorem world_bank_macro_open_observable_count_pos : 0 < world_bank_macro_open_observable_count := by
  unfold world_bank_macro_open_observable_count; norm_num

theorem world_bank_macro_open_pooled_median_under_half_pct :
    world_bank_macro_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold world_bank_macro_open_pooled_median_error_pct; norm_num

theorem world_bank_macro_open_headline_median_under_half_pct :
    world_bank_macro_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold world_bank_macro_open_headline_median_error_pct; norm_num

theorem world_bank_macro_open_bundle :
    world_bank_macro_open_observable_count = 605 ∧
    world_bank_macro_open_D_eff = 18 ∧
    world_bank_macro_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold world_bank_macro_open_observable_count; norm_num
  · unfold world_bank_macro_open_D_eff; norm_num
  · exact world_bank_macro_open_pooled_median_under_half_pct

end
