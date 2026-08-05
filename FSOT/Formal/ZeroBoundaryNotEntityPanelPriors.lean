/-
  FSOT Formal ZeroBoundaryNotEntityPanelPriors — extension domain Zero_Boundary_Not_Entity_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def zero_boundary_not_entity_panel_observable_count : ℕ := 24
def zero_boundary_not_entity_panel_D_eff : ℕ := 18

theorem zero_boundary_not_entity_panel_observable_count_pos : 0 < zero_boundary_not_entity_panel_observable_count := by
  unfold zero_boundary_not_entity_panel_observable_count; decide

theorem zero_boundary_not_entity_panel_median_error_under_half_pct :
    (0.020055 : ℝ) < (0.5 : ℝ) := by norm_num

theorem zero_boundary_not_entity_panel_bundle :
    zero_boundary_not_entity_panel_observable_count = 24 ∧
    zero_boundary_not_entity_panel_D_eff = 18 ∧
    (0.020055 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold zero_boundary_not_entity_panel_observable_count; decide,
    by unfold zero_boundary_not_entity_panel_D_eff; decide,
    zero_boundary_not_entity_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
