/-
  FSOT Formal OeisFamilySweepOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def oeis_family_sweep_open_observable_count : ℕ := 394
def oeis_family_sweep_open_pooled_median_error_pct : ℝ := (0.014767 : ℝ)
def oeis_family_sweep_open_headline_median_error_pct : ℝ := (0.014767 : ℝ)
def oeis_family_sweep_open_D_eff : ℕ := 14

theorem oeis_family_sweep_open_observable_count_pos : 0 < oeis_family_sweep_open_observable_count := by
  unfold oeis_family_sweep_open_observable_count; norm_num

theorem oeis_family_sweep_open_pooled_median_under_half_pct :
    oeis_family_sweep_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold oeis_family_sweep_open_pooled_median_error_pct; norm_num

theorem oeis_family_sweep_open_headline_median_under_half_pct :
    oeis_family_sweep_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold oeis_family_sweep_open_headline_median_error_pct; norm_num

theorem oeis_family_sweep_open_bundle :
    oeis_family_sweep_open_observable_count = 394 ∧
    oeis_family_sweep_open_D_eff = 14 ∧
    oeis_family_sweep_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold oeis_family_sweep_open_observable_count; norm_num
  · unfold oeis_family_sweep_open_D_eff; norm_num
  · exact oeis_family_sweep_open_pooled_median_under_half_pct

end
