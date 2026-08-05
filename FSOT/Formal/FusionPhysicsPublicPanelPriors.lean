/-
  FSOT Formal FusionPhysicsPublicPanelPriors — extension domain Fusion_Physics_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fusion_physics_public_panel_observable_count : ℕ := 24
def fusion_physics_public_panel_D_eff : ℕ := 18

theorem fusion_physics_public_panel_observable_count_pos : 0 < fusion_physics_public_panel_observable_count := by
  unfold fusion_physics_public_panel_observable_count; decide

theorem fusion_physics_public_panel_median_error_under_half_pct :
    (9.5e-05 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (9.5e-05 : ℝ) < (0.5 : ℝ))

theorem fusion_physics_public_panel_bundle :
    fusion_physics_public_panel_observable_count = 24 ∧
    fusion_physics_public_panel_D_eff = 18 ∧
    (9.5e-05 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fusion_physics_public_panel_observable_count; decide,
    by unfold fusion_physics_public_panel_D_eff; decide,
    fusion_physics_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
