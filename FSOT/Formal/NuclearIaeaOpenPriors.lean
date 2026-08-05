/-
  FSOT Formal NuclearIaeaOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def nuclear_iaea_open_observable_count : ℕ := 360
def nuclear_iaea_open_pooled_median_error_pct : ℝ := (0.092131 : ℝ)
def nuclear_iaea_open_headline_median_error_pct : ℝ := (0.092131 : ℝ)
def nuclear_iaea_open_D_eff : ℕ := 16

theorem nuclear_iaea_open_observable_count_pos : 0 < nuclear_iaea_open_observable_count := by
  unfold nuclear_iaea_open_observable_count; norm_num

theorem nuclear_iaea_open_pooled_median_under_half_pct :
    nuclear_iaea_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold nuclear_iaea_open_pooled_median_error_pct; norm_num

theorem nuclear_iaea_open_headline_median_under_half_pct :
    nuclear_iaea_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold nuclear_iaea_open_headline_median_error_pct; norm_num

theorem nuclear_iaea_open_bundle :
    nuclear_iaea_open_observable_count = 360 ∧
    nuclear_iaea_open_D_eff = 16 ∧
    nuclear_iaea_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold nuclear_iaea_open_observable_count; norm_num
  · unfold nuclear_iaea_open_D_eff; norm_num
  · exact nuclear_iaea_open_pooled_median_under_half_pct

end
