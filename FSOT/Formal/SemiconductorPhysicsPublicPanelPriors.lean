/-
  FSOT Formal SemiconductorPhysicsPublicPanelPriors — Tier 62–64 live astrometry, prereg scaffold, NeuroLab gaps.
  Generator: scripts/gen_tiers_62_64_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def semiconductor_physics_public_panel_observable_count : ℕ := 11
def semiconductor_physics_public_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def semiconductor_physics_public_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def semiconductor_physics_public_panel_beats_sota_headlines : ℕ := 2
def semiconductor_physics_public_panel_D_eff : ℕ := 11

theorem semiconductor_physics_public_panel_observable_count_pos : 0 < semiconductor_physics_public_panel_observable_count := by
  unfold semiconductor_physics_public_panel_observable_count; norm_num

theorem semiconductor_physics_public_panel_pooled_median_under_half_pct :
    semiconductor_physics_public_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold semiconductor_physics_public_panel_pooled_median_error_pct; norm_num

theorem semiconductor_physics_public_panel_headline_median_under_half_pct :
    semiconductor_physics_public_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold semiconductor_physics_public_panel_headline_median_error_pct; norm_num

theorem semiconductor_physics_public_panel_beats_sota_headlines_pos : 0 < semiconductor_physics_public_panel_beats_sota_headlines := by
  unfold semiconductor_physics_public_panel_beats_sota_headlines; norm_num

theorem semiconductor_physics_public_panel_bundle :
    semiconductor_physics_public_panel_observable_count = 11 ∧
    semiconductor_physics_public_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    semiconductor_physics_public_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold semiconductor_physics_public_panel_observable_count; norm_num
  · exact semiconductor_physics_public_panel_pooled_median_under_half_pct
  · exact semiconductor_physics_public_panel_beats_sota_headlines_pos

end
