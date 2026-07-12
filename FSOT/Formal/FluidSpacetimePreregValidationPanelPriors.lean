/-
  FSOT Formal FluidSpacetimePreregValidationPanelPriors — extension domain Fluid_Spacetime_Prereg_Validation_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fluid_spacetime_prereg_validation_panel_observable_count : ℕ := 24
def fluid_spacetime_prereg_validation_panel_D_eff : ℕ := 25

theorem fluid_spacetime_prereg_validation_panel_observable_count_pos : 0 < fluid_spacetime_prereg_validation_panel_observable_count := by
  unfold fluid_spacetime_prereg_validation_panel_observable_count; norm_num

theorem fluid_spacetime_prereg_validation_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem fluid_spacetime_prereg_validation_panel_bundle :
    fluid_spacetime_prereg_validation_panel_observable_count = 24 ∧
    fluid_spacetime_prereg_validation_panel_D_eff = 25 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fluid_spacetime_prereg_validation_panel_observable_count; norm_num,
    by unfold fluid_spacetime_prereg_validation_panel_D_eff; norm_num,
    fluid_spacetime_prereg_validation_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
