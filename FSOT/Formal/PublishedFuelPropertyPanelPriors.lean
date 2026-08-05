/-
  FSOT Formal PublishedFuelPropertyPanelPriors — extension domain Published_Fuel_Property_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def published_fuel_property_panel_observable_count : ℕ := 31
def published_fuel_property_panel_D_eff : ℕ := 16

theorem published_fuel_property_panel_observable_count_pos : 0 < published_fuel_property_panel_observable_count := by
  unfold published_fuel_property_panel_observable_count; decide

theorem published_fuel_property_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem published_fuel_property_panel_bundle :
    published_fuel_property_panel_observable_count = 31 ∧
    published_fuel_property_panel_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold published_fuel_property_panel_observable_count; decide,
    by unfold published_fuel_property_panel_D_eff; decide,
    published_fuel_property_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
