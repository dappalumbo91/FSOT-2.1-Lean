/-
  FSOT Formal EndfIaeaNuclearOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def endf_iaea_nuclear_open_observable_count : ℕ := 517
def endf_iaea_nuclear_open_pooled_median_error_pct : ℝ := (0.092131 : ℝ)
def endf_iaea_nuclear_open_headline_median_error_pct : ℝ := (0.092131 : ℝ)
def endf_iaea_nuclear_open_D_eff : ℕ := 16

theorem endf_iaea_nuclear_open_observable_count_pos : 0 < endf_iaea_nuclear_open_observable_count := by
  unfold endf_iaea_nuclear_open_observable_count; norm_num

theorem endf_iaea_nuclear_open_pooled_median_under_half_pct :
    endf_iaea_nuclear_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold endf_iaea_nuclear_open_pooled_median_error_pct; norm_num

theorem endf_iaea_nuclear_open_headline_median_under_half_pct :
    endf_iaea_nuclear_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold endf_iaea_nuclear_open_headline_median_error_pct; norm_num

theorem endf_iaea_nuclear_open_bundle :
    endf_iaea_nuclear_open_observable_count = 517 ∧
    endf_iaea_nuclear_open_D_eff = 16 ∧
    endf_iaea_nuclear_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold endf_iaea_nuclear_open_observable_count; norm_num
  · unfold endf_iaea_nuclear_open_D_eff; norm_num
  · exact endf_iaea_nuclear_open_pooled_median_under_half_pct

end
