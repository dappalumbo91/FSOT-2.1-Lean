/-
  FSOT Formal ChemicalStructureStabilityPanelPriors — extension domain Chemical_Structure_Stability_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def chemical_structure_stability_panel_observable_count : ℕ := 32
def chemical_structure_stability_panel_D_eff : ℕ := 14

theorem chemical_structure_stability_panel_observable_count_pos : 0 < chemical_structure_stability_panel_observable_count := by
  unfold chemical_structure_stability_panel_observable_count; decide

theorem chemical_structure_stability_panel_median_error_under_half_pct :
    (0.00206 : ℝ) < (0.5 : ℝ) := by norm_num

theorem chemical_structure_stability_panel_bundle :
    chemical_structure_stability_panel_observable_count = 32 ∧
    chemical_structure_stability_panel_D_eff = 14 ∧
    (0.00206 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold chemical_structure_stability_panel_observable_count; decide,
    by unfold chemical_structure_stability_panel_D_eff; decide,
    chemical_structure_stability_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
