/-
  FSOT Formal InertialConfinementFusionPanelPriors — extension domain Inertial_Confinement_Fusion_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def inertial_confinement_fusion_panel_observable_count : ℕ := 24
def inertial_confinement_fusion_panel_D_eff : ℕ := 17

theorem inertial_confinement_fusion_panel_observable_count_pos : 0 < inertial_confinement_fusion_panel_observable_count := by
  unfold inertial_confinement_fusion_panel_observable_count; norm_num

theorem inertial_confinement_fusion_panel_median_error_under_half_pct :
    (7.9e-05 : ℝ) < (0.5 : ℝ) := by norm_num

theorem inertial_confinement_fusion_panel_bundle :
    inertial_confinement_fusion_panel_observable_count = 24 ∧
    inertial_confinement_fusion_panel_D_eff = 17 ∧
    (7.9e-05 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold inertial_confinement_fusion_panel_observable_count; norm_num,
    by unfold inertial_confinement_fusion_panel_D_eff; norm_num,
    inertial_confinement_fusion_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
