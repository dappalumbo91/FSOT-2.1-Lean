/-
  FSOT Formal NoaaTidesMultiStationOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def noaa_tides_multi_station_open_observable_count : ℕ := 209
def noaa_tides_multi_station_open_pooled_median_error_pct : ℝ := (0.030173 : ℝ)
def noaa_tides_multi_station_open_headline_median_error_pct : ℝ := (0.030173 : ℝ)
def noaa_tides_multi_station_open_D_eff : ℕ := 16

theorem noaa_tides_multi_station_open_observable_count_pos : 0 < noaa_tides_multi_station_open_observable_count := by
  unfold noaa_tides_multi_station_open_observable_count; decide

theorem noaa_tides_multi_station_open_pooled_median_under_half_pct :
    noaa_tides_multi_station_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold noaa_tides_multi_station_open_pooled_median_error_pct
  exact (by norm_num : (0.030173  : ℝ) < 0.5)

theorem noaa_tides_multi_station_open_headline_median_under_half_pct :
    noaa_tides_multi_station_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold noaa_tides_multi_station_open_headline_median_error_pct
  exact (by norm_num : (0.030173  : ℝ) < 0.5)

theorem noaa_tides_multi_station_open_bundle :
    noaa_tides_multi_station_open_observable_count = 209 ∧
    noaa_tides_multi_station_open_D_eff = 16 ∧
    noaa_tides_multi_station_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold noaa_tides_multi_station_open_observable_count; decide
  · unfold noaa_tides_multi_station_open_D_eff; decide
  · exact noaa_tides_multi_station_open_pooled_median_under_half_pct

end
