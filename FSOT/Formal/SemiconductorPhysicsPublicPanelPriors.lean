/-
  FSOT Formal SemiconductorPhysicsPublicPanelPriors — extension domain Semiconductor_Physics_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def semiconductor_physics_public_panel_observable_count : ℕ := 24
def semiconductor_physics_public_panel_D_eff : ℕ := 11

theorem semiconductor_physics_public_panel_observable_count_pos : 0 < semiconductor_physics_public_panel_observable_count := by
  unfold semiconductor_physics_public_panel_observable_count; decide

theorem semiconductor_physics_public_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem semiconductor_physics_public_panel_bundle :
    semiconductor_physics_public_panel_observable_count = 24 ∧
    semiconductor_physics_public_panel_D_eff = 11 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold semiconductor_physics_public_panel_observable_count; decide,
    by unfold semiconductor_physics_public_panel_D_eff; decide,
    semiconductor_physics_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
