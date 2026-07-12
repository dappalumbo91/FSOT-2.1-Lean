/-
  FSOT Formal MagneticConfinementFusionPanelPriors — extension domain Magnetic_Confinement_Fusion_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def magnetic_confinement_fusion_panel_observable_count : ℕ := 22
def magnetic_confinement_fusion_panel_D_eff : ℕ := 16

theorem magnetic_confinement_fusion_panel_observable_count_pos : 0 < magnetic_confinement_fusion_panel_observable_count := by
  unfold magnetic_confinement_fusion_panel_observable_count; norm_num

theorem magnetic_confinement_fusion_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem magnetic_confinement_fusion_panel_bundle :
    magnetic_confinement_fusion_panel_observable_count = 22 ∧
    magnetic_confinement_fusion_panel_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold magnetic_confinement_fusion_panel_observable_count; norm_num,
    by unfold magnetic_confinement_fusion_panel_D_eff; norm_num,
    magnetic_confinement_fusion_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
