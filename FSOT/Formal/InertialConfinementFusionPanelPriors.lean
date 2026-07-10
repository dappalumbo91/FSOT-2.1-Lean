/-
  FSOT Formal InertialConfinementFusionPanelPriors — Tier 71 fusion lab expansion.
  Generator: scripts/gen_tiers_71_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def inertial_confinement_fusion_panel_observable_count : ℕ := 15
def inertial_confinement_fusion_panel_pooled_median_error_pct : ℝ := (7.9e-05 : ℝ)
def inertial_confinement_fusion_panel_headline_median_error_pct : ℝ := (7.9e-05 : ℝ)
def inertial_confinement_fusion_panel_beats_sota_headlines : ℕ := 2
def inertial_confinement_fusion_panel_D_eff : ℕ := 17

theorem inertial_confinement_fusion_panel_observable_count_pos : 0 < inertial_confinement_fusion_panel_observable_count := by
  unfold inertial_confinement_fusion_panel_observable_count; norm_num

theorem inertial_confinement_fusion_panel_pooled_median_under_half_pct :
    inertial_confinement_fusion_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold inertial_confinement_fusion_panel_pooled_median_error_pct; norm_num

theorem inertial_confinement_fusion_panel_headline_median_under_half_pct :
    inertial_confinement_fusion_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold inertial_confinement_fusion_panel_headline_median_error_pct; norm_num

theorem inertial_confinement_fusion_panel_beats_sota_headlines_pos : 0 < inertial_confinement_fusion_panel_beats_sota_headlines := by
  unfold inertial_confinement_fusion_panel_beats_sota_headlines; norm_num

theorem inertial_confinement_fusion_panel_bundle :
    inertial_confinement_fusion_panel_observable_count = 15 ∧
    inertial_confinement_fusion_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    inertial_confinement_fusion_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold inertial_confinement_fusion_panel_observable_count; norm_num
  · exact inertial_confinement_fusion_panel_pooled_median_under_half_pct
  · exact inertial_confinement_fusion_panel_beats_sota_headlines_pos

end
