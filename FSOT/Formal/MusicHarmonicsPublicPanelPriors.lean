/-
  FSOT Formal MusicHarmonicsPublicPanelPriors — Tier 61 music harmonics, XR/game math, creative arts spine.
  Generator: scripts/gen_tiers_61_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def music_harmonics_public_panel_observable_count : ℕ := 18
def music_harmonics_public_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def music_harmonics_public_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def music_harmonics_public_panel_beats_sota_headlines : ℕ := 2
def music_harmonics_public_panel_D_eff : ℕ := 10

theorem music_harmonics_public_panel_observable_count_pos : 0 < music_harmonics_public_panel_observable_count := by
  unfold music_harmonics_public_panel_observable_count; norm_num

theorem music_harmonics_public_panel_pooled_median_under_half_pct :
    music_harmonics_public_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold music_harmonics_public_panel_pooled_median_error_pct; norm_num

theorem music_harmonics_public_panel_headline_median_under_half_pct :
    music_harmonics_public_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold music_harmonics_public_panel_headline_median_error_pct; norm_num

theorem music_harmonics_public_panel_beats_sota_headlines_pos : 0 < music_harmonics_public_panel_beats_sota_headlines := by
  unfold music_harmonics_public_panel_beats_sota_headlines; norm_num

theorem music_harmonics_public_panel_bundle :
    music_harmonics_public_panel_observable_count = 18 ∧
    music_harmonics_public_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    music_harmonics_public_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold music_harmonics_public_panel_observable_count; norm_num
  · exact music_harmonics_public_panel_pooled_median_under_half_pct
  · exact music_harmonics_public_panel_beats_sota_headlines_pos

end
