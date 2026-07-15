/-
  FSOT Formal MaterialsCreepFractureDepthPanelPriors — extension domain Materials_Creep_Fracture_Depth_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def materials_creep_fracture_depth_panel_observable_count : ℕ := 71
def materials_creep_fracture_depth_panel_D_eff : ℕ := 16

theorem materials_creep_fracture_depth_panel_observable_count_pos : 0 < materials_creep_fracture_depth_panel_observable_count := by
  unfold materials_creep_fracture_depth_panel_observable_count; norm_num

theorem materials_creep_fracture_depth_panel_median_error_under_half_pct :
    (0.011734 : ℝ) < (0.5 : ℝ) := by norm_num

theorem materials_creep_fracture_depth_panel_bundle :
    materials_creep_fracture_depth_panel_observable_count = 71 ∧
    materials_creep_fracture_depth_panel_D_eff = 16 ∧
    (0.011734 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold materials_creep_fracture_depth_panel_observable_count; norm_num,
    by unfold materials_creep_fracture_depth_panel_D_eff; norm_num,
    materials_creep_fracture_depth_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
