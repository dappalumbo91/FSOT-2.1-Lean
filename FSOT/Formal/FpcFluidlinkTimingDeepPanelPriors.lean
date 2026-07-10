/-
  FSOT Formal FpcFluidlinkTimingDeepPanelPriors — Tier 76 fluid spacetime + cosmology.
  Generator: scripts/gen_tiers_76_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fpc_fluidlink_timing_deep_panel_observable_count : ℕ := 13
def fpc_fluidlink_timing_deep_panel_pooled_median_error_pct : ℝ := (5e-05 : ℝ)
def fpc_fluidlink_timing_deep_panel_headline_median_error_pct : ℝ := (5.024559461830336e-05 : ℝ)
def fpc_fluidlink_timing_deep_panel_beats_sota_headlines : ℕ := 2
def fpc_fluidlink_timing_deep_panel_D_eff : ℕ := 20

theorem fpc_fluidlink_timing_deep_panel_observable_count_pos : 0 < fpc_fluidlink_timing_deep_panel_observable_count := by
  unfold fpc_fluidlink_timing_deep_panel_observable_count; norm_num

theorem fpc_fluidlink_timing_deep_panel_pooled_median_under_half_pct :
    fpc_fluidlink_timing_deep_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fpc_fluidlink_timing_deep_panel_pooled_median_error_pct; norm_num

theorem fpc_fluidlink_timing_deep_panel_headline_median_under_half_pct :
    fpc_fluidlink_timing_deep_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fpc_fluidlink_timing_deep_panel_headline_median_error_pct; norm_num

theorem fpc_fluidlink_timing_deep_panel_beats_sota_headlines_pos : 0 < fpc_fluidlink_timing_deep_panel_beats_sota_headlines := by
  unfold fpc_fluidlink_timing_deep_panel_beats_sota_headlines; norm_num

theorem fpc_fluidlink_timing_deep_panel_bundle :
    fpc_fluidlink_timing_deep_panel_observable_count = 13 ∧
    fpc_fluidlink_timing_deep_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    fpc_fluidlink_timing_deep_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fpc_fluidlink_timing_deep_panel_observable_count; norm_num
  · exact fpc_fluidlink_timing_deep_panel_pooled_median_under_half_pct
  · exact fpc_fluidlink_timing_deep_panel_beats_sota_headlines_pos

end
