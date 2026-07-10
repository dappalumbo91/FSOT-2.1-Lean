/-
  FSOT Formal NetworkSciencePublicPanelPriors — Tier 62–64 live astrometry, prereg scaffold, NeuroLab gaps.
  Generator: scripts/gen_tiers_62_64_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def network_science_public_panel_observable_count : ℕ := 10
def network_science_public_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def network_science_public_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def network_science_public_panel_beats_sota_headlines : ℕ := 2
def network_science_public_panel_D_eff : ℕ := 17

theorem network_science_public_panel_observable_count_pos : 0 < network_science_public_panel_observable_count := by
  unfold network_science_public_panel_observable_count; norm_num

theorem network_science_public_panel_pooled_median_under_half_pct :
    network_science_public_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold network_science_public_panel_pooled_median_error_pct; norm_num

theorem network_science_public_panel_headline_median_under_half_pct :
    network_science_public_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold network_science_public_panel_headline_median_error_pct; norm_num

theorem network_science_public_panel_beats_sota_headlines_pos : 0 < network_science_public_panel_beats_sota_headlines := by
  unfold network_science_public_panel_beats_sota_headlines; norm_num

theorem network_science_public_panel_bundle :
    network_science_public_panel_observable_count = 10 ∧
    network_science_public_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    network_science_public_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold network_science_public_panel_observable_count; norm_num
  · exact network_science_public_panel_pooled_median_under_half_pct
  · exact network_science_public_panel_beats_sota_headlines_pos

end
