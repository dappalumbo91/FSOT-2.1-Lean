/-
  FSOT Formal FusionPhysicsPublicPanelPriors — Tier 71 fusion lab expansion.
  Generator: scripts/gen_tiers_71_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fusion_physics_public_panel_observable_count : ℕ := 19
def fusion_physics_public_panel_pooled_median_error_pct : ℝ := (9.5e-05 : ℝ)
def fusion_physics_public_panel_headline_median_error_pct : ℝ := (9.50413440155747e-05 : ℝ)
def fusion_physics_public_panel_beats_sota_headlines : ℕ := 2
def fusion_physics_public_panel_D_eff : ℕ := 18

theorem fusion_physics_public_panel_observable_count_pos : 0 < fusion_physics_public_panel_observable_count := by
  unfold fusion_physics_public_panel_observable_count; norm_num

theorem fusion_physics_public_panel_pooled_median_under_half_pct :
    fusion_physics_public_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fusion_physics_public_panel_pooled_median_error_pct; norm_num

theorem fusion_physics_public_panel_headline_median_under_half_pct :
    fusion_physics_public_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fusion_physics_public_panel_headline_median_error_pct; norm_num

theorem fusion_physics_public_panel_beats_sota_headlines_pos : 0 < fusion_physics_public_panel_beats_sota_headlines := by
  unfold fusion_physics_public_panel_beats_sota_headlines; norm_num

theorem fusion_physics_public_panel_bundle :
    fusion_physics_public_panel_observable_count = 19 ∧
    fusion_physics_public_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    fusion_physics_public_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fusion_physics_public_panel_observable_count; norm_num
  · exact fusion_physics_public_panel_pooled_median_under_half_pct
  · exact fusion_physics_public_panel_beats_sota_headlines_pos

end
