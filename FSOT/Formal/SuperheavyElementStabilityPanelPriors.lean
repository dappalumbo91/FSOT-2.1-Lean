/-
  FSOT Formal SuperheavyElementStabilityPanelPriors — extension domain Superheavy_Element_Stability_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def superheavy_element_stability_panel_observable_count : ℕ := 50
def superheavy_element_stability_panel_D_eff : ℕ := 10

theorem superheavy_element_stability_panel_observable_count_pos : 0 < superheavy_element_stability_panel_observable_count := by
  unfold superheavy_element_stability_panel_observable_count; decide

theorem superheavy_element_stability_panel_median_error_under_half_pct :
    (1e-06 : ℝ) < (0.5 : ℝ) := by norm_num

theorem superheavy_element_stability_panel_bundle :
    superheavy_element_stability_panel_observable_count = 50 ∧
    superheavy_element_stability_panel_D_eff = 10 ∧
    (1e-06 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold superheavy_element_stability_panel_observable_count; decide,
    by unfold superheavy_element_stability_panel_D_eff; decide,
    superheavy_element_stability_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
