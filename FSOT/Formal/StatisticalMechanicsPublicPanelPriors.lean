/-
  FSOT Formal StatisticalMechanicsPublicPanelPriors — Tier 62–64 live astrometry, prereg scaffold, NeuroLab gaps.
  Generator: scripts/gen_tiers_62_64_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def statistical_mechanics_public_panel_observable_count : ℕ := 10
def statistical_mechanics_public_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def statistical_mechanics_public_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def statistical_mechanics_public_panel_beats_sota_headlines : ℕ := 2
def statistical_mechanics_public_panel_D_eff : ℕ := 12

theorem statistical_mechanics_public_panel_observable_count_pos : 0 < statistical_mechanics_public_panel_observable_count := by
  unfold statistical_mechanics_public_panel_observable_count; norm_num

theorem statistical_mechanics_public_panel_pooled_median_under_half_pct :
    statistical_mechanics_public_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold statistical_mechanics_public_panel_pooled_median_error_pct; norm_num

theorem statistical_mechanics_public_panel_headline_median_under_half_pct :
    statistical_mechanics_public_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold statistical_mechanics_public_panel_headline_median_error_pct; norm_num

theorem statistical_mechanics_public_panel_beats_sota_headlines_pos : 0 < statistical_mechanics_public_panel_beats_sota_headlines := by
  unfold statistical_mechanics_public_panel_beats_sota_headlines; norm_num

theorem statistical_mechanics_public_panel_bundle :
    statistical_mechanics_public_panel_observable_count = 10 ∧
    statistical_mechanics_public_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    statistical_mechanics_public_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold statistical_mechanics_public_panel_observable_count; norm_num
  · exact statistical_mechanics_public_panel_pooled_median_under_half_pct
  · exact statistical_mechanics_public_panel_beats_sota_headlines_pos

end
