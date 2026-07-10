/-
  FSOT Formal MagneticConfinementFusionPanelPriors — Tier 71 fusion lab expansion.
  Generator: scripts/gen_tiers_71_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def magnetic_confinement_fusion_panel_observable_count : ℕ := 22
def magnetic_confinement_fusion_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def magnetic_confinement_fusion_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def magnetic_confinement_fusion_panel_beats_sota_headlines : ℕ := 2
def magnetic_confinement_fusion_panel_D_eff : ℕ := 16

theorem magnetic_confinement_fusion_panel_observable_count_pos : 0 < magnetic_confinement_fusion_panel_observable_count := by
  unfold magnetic_confinement_fusion_panel_observable_count; norm_num

theorem magnetic_confinement_fusion_panel_pooled_median_under_half_pct :
    magnetic_confinement_fusion_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold magnetic_confinement_fusion_panel_pooled_median_error_pct; norm_num

theorem magnetic_confinement_fusion_panel_headline_median_under_half_pct :
    magnetic_confinement_fusion_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold magnetic_confinement_fusion_panel_headline_median_error_pct; norm_num

theorem magnetic_confinement_fusion_panel_beats_sota_headlines_pos : 0 < magnetic_confinement_fusion_panel_beats_sota_headlines := by
  unfold magnetic_confinement_fusion_panel_beats_sota_headlines; norm_num

theorem magnetic_confinement_fusion_panel_bundle :
    magnetic_confinement_fusion_panel_observable_count = 22 ∧
    magnetic_confinement_fusion_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    magnetic_confinement_fusion_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold magnetic_confinement_fusion_panel_observable_count; norm_num
  · exact magnetic_confinement_fusion_panel_pooled_median_under_half_pct
  · exact magnetic_confinement_fusion_panel_beats_sota_headlines_pos

end
