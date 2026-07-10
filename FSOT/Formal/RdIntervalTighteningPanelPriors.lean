/-
  FSOT Formal RdIntervalTighteningPanelPriors — Tier 77 post–Tier 76 maintenance.
  Generator: scripts/gen_tiers_77_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def rd_interval_tightening_panel_observable_count : ℕ := 12
def rd_interval_tightening_panel_pooled_median_error_pct : ℝ := (0.000502 : ℝ)
def rd_interval_tightening_panel_headline_median_error_pct : ℝ := (0.005024559462094211 : ℝ)
def rd_interval_tightening_panel_beats_sota_headlines : ℕ := 2
def rd_interval_tightening_panel_D_eff : ℕ := 22

theorem rd_interval_tightening_panel_observable_count_pos : 0 < rd_interval_tightening_panel_observable_count := by
  unfold rd_interval_tightening_panel_observable_count; norm_num

theorem rd_interval_tightening_panel_pooled_median_under_half_pct :
    rd_interval_tightening_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold rd_interval_tightening_panel_pooled_median_error_pct; norm_num

theorem rd_interval_tightening_panel_headline_median_under_half_pct :
    rd_interval_tightening_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold rd_interval_tightening_panel_headline_median_error_pct; norm_num

theorem rd_interval_tightening_panel_beats_sota_headlines_pos : 0 < rd_interval_tightening_panel_beats_sota_headlines := by
  unfold rd_interval_tightening_panel_beats_sota_headlines; norm_num

theorem rd_interval_tightening_panel_bundle :
    rd_interval_tightening_panel_observable_count = 12 ∧
    rd_interval_tightening_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    rd_interval_tightening_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold rd_interval_tightening_panel_observable_count; norm_num
  · exact rd_interval_tightening_panel_pooled_median_under_half_pct
  · exact rd_interval_tightening_panel_beats_sota_headlines_pos

end
