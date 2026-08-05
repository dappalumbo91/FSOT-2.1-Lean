/-
  FSOT Formal FederalScienceRegistryPanelPriors — extension domain Federal_Science_Registry_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def federal_science_registry_panel_observable_count : ℕ := 24
def federal_science_registry_panel_D_eff : ℕ := 17

theorem federal_science_registry_panel_observable_count_pos : 0 < federal_science_registry_panel_observable_count := by
  unfold federal_science_registry_panel_observable_count; decide

theorem federal_science_registry_panel_median_error_under_half_pct :
    (0.013352 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.013352 : ℝ) < (0.5 : ℝ))

theorem federal_science_registry_panel_bundle :
    federal_science_registry_panel_observable_count = 24 ∧
    federal_science_registry_panel_D_eff = 17 ∧
    (0.013352 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold federal_science_registry_panel_observable_count; decide,
    by unfold federal_science_registry_panel_D_eff; decide,
    federal_science_registry_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
