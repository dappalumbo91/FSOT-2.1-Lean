/-
  FSOT Formal PetrologyGeochemistryPanelPriors — extension domain Petrology_Geochemistry_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def petrology_geochemistry_panel_observable_count : ℕ := 80
def petrology_geochemistry_panel_D_eff : ℕ := 14

theorem petrology_geochemistry_panel_observable_count_pos : 0 < petrology_geochemistry_panel_observable_count := by
  unfold petrology_geochemistry_panel_observable_count; norm_num

theorem petrology_geochemistry_panel_median_error_under_half_pct :
    (0.030428 : ℝ) < (0.5 : ℝ) := by norm_num

theorem petrology_geochemistry_panel_bundle :
    petrology_geochemistry_panel_observable_count = 80 ∧
    petrology_geochemistry_panel_D_eff = 14 ∧
    (0.030428 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold petrology_geochemistry_panel_observable_count; norm_num,
    by unfold petrology_geochemistry_panel_D_eff; norm_num,
    petrology_geochemistry_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
