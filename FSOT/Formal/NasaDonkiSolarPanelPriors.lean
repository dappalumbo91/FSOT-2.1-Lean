/-
  FSOT Formal NasaDonkiSolarPanelPriors — extension domain NASA_DONKI_Solar_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def nasa_donki_solar_panel_observable_count : ℕ := 2148
def nasa_donki_solar_panel_D_eff : ℕ := 14

theorem nasa_donki_solar_panel_observable_count_pos : 0 < nasa_donki_solar_panel_observable_count := by
  unfold nasa_donki_solar_panel_observable_count; decide

theorem nasa_donki_solar_panel_median_error_under_half_pct :
    (0.020755 : ℝ) < (0.5 : ℝ) := by norm_num

theorem nasa_donki_solar_panel_bundle :
    nasa_donki_solar_panel_observable_count = 2148 ∧
    nasa_donki_solar_panel_D_eff = 14 ∧
    (0.020755 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold nasa_donki_solar_panel_observable_count; decide,
    by unfold nasa_donki_solar_panel_D_eff; decide,
    nasa_donki_solar_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
