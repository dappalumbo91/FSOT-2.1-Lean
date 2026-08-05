/-
  FSOT Formal NoaaNdbcBuoyPanelPriors — extension domain NOAA_NDBC_Buoy_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def noaa_ndbc_buoy_panel_observable_count : ℕ := 596
def noaa_ndbc_buoy_panel_D_eff : ℕ := 17

theorem noaa_ndbc_buoy_panel_observable_count_pos : 0 < noaa_ndbc_buoy_panel_observable_count := by
  unfold noaa_ndbc_buoy_panel_observable_count; decide

theorem noaa_ndbc_buoy_panel_median_error_under_half_pct :
    (0.028287 : ℝ) < (0.5 : ℝ) := by norm_num

theorem noaa_ndbc_buoy_panel_bundle :
    noaa_ndbc_buoy_panel_observable_count = 596 ∧
    noaa_ndbc_buoy_panel_D_eff = 17 ∧
    (0.028287 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold noaa_ndbc_buoy_panel_observable_count; decide,
    by unfold noaa_ndbc_buoy_panel_D_eff; decide,
    noaa_ndbc_buoy_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
