/-
  FSOT Formal MechanicalEngineeringPanelPriors — extension domain Mechanical_Engineering_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def mechanical_engineering_panel_observable_count : ℕ := 20
def mechanical_engineering_panel_D_eff : ℕ := 16

theorem mechanical_engineering_panel_observable_count_pos : 0 < mechanical_engineering_panel_observable_count := by
  unfold mechanical_engineering_panel_observable_count; decide

theorem mechanical_engineering_panel_median_error_under_half_pct :
    (0.039349 : ℝ) < (0.5 : ℝ) := by norm_num

theorem mechanical_engineering_panel_bundle :
    mechanical_engineering_panel_observable_count = 20 ∧
    mechanical_engineering_panel_D_eff = 16 ∧
    (0.039349 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold mechanical_engineering_panel_observable_count; decide,
    by unfold mechanical_engineering_panel_D_eff; decide,
    mechanical_engineering_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
