/-
  FSOT Formal MechanicalEngineeringPanelPriors — Tier 85 scientific expansion (Mechanical_Engineering_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def mechanical_engineering_panel_observable_count : ℕ := 20
def mechanical_engineering_panel_median_error_pct : ℝ := (0.078697 : ℝ)
def mechanical_engineering_panel_D_eff : ℕ := 16

theorem mechanical_engineering_panel_observable_count_pos : 0 < mechanical_engineering_panel_observable_count := by
  unfold mechanical_engineering_panel_observable_count; norm_num

theorem mechanical_engineering_panel_median_error_under_five_pct :
    mechanical_engineering_panel_median_error_pct < (5 : ℝ) := by
  unfold mechanical_engineering_panel_median_error_pct; norm_num

theorem mechanical_engineering_panel_bundle :
    mechanical_engineering_panel_observable_count = 20 ∧
    mechanical_engineering_panel_D_eff = 16 ∧
    mechanical_engineering_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold mechanical_engineering_panel_observable_count; norm_num,
    by unfold mechanical_engineering_panel_D_eff; norm_num,
    mechanical_engineering_panel_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
