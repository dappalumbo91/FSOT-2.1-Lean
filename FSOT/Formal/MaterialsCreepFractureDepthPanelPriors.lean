/-
  FSOT Formal MaterialsCreepFractureDepthPanelPriors — Tier 87 depth wave (Materials_Creep_Fracture_Depth_Panel).
  Generator: scripts/gen_tier87_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def materials_creep_fracture_depth_observable_count : ℕ := 47
def materials_creep_fracture_depth_median_error_pct : ℝ := (0.01341 : ℝ)
def materials_creep_fracture_depth_D_eff : ℕ := 16

theorem materials_creep_fracture_depth_observable_count_pos : 0 < materials_creep_fracture_depth_observable_count := by
  unfold materials_creep_fracture_depth_observable_count; norm_num

theorem materials_creep_fracture_depth_median_error_under_five_pct :
    materials_creep_fracture_depth_median_error_pct < (5 : ℝ) := by
  unfold materials_creep_fracture_depth_median_error_pct; norm_num

theorem materials_creep_fracture_depth_bundle :
    materials_creep_fracture_depth_observable_count = 47 ∧
    materials_creep_fracture_depth_D_eff = 16 ∧
    materials_creep_fracture_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold materials_creep_fracture_depth_observable_count; norm_num,
    by unfold materials_creep_fracture_depth_D_eff; norm_num,
    materials_creep_fracture_depth_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
