/-
  FSOT Formal SpaceWeatherPriors — NOAA SWPC Kp/Ap space weather observables.
  Generator: scripts/gen_space_weather_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def space_weather_kp_record_count : ℕ := 271813
def space_weather_ap_record_count : ℕ := 271813
def space_weather_stability_match_count : ℕ := 271813
def space_weather_D_eff : ℕ := 14
def space_weather_stability_match_rate : ℝ := (1.0 : ℝ)

theorem space_weather_kp_record_count_pos : 0 < space_weather_kp_record_count := by
  unfold space_weather_kp_record_count; decide

theorem space_weather_stability_match_le_total :
    space_weather_stability_match_count ≤ space_weather_kp_record_count := by
  unfold space_weather_stability_match_count space_weather_kp_record_count; decide

theorem space_weather_stability_match_rate_nonneg : (0 : ℝ) ≤ space_weather_stability_match_rate := by
  unfold space_weather_stability_match_rate; norm_num

/-- Bundle: NOAA Kp storm classifier bridged to fusion-domain sign proxy. -/
theorem space_weather_bundle :
    space_weather_kp_record_count = 271813 ∧
    space_weather_ap_record_count = 271813 ∧
    space_weather_stability_match_count = 271813 ∧
    space_weather_D_eff = 14 ∧
    space_weather_stability_match_count ≤ space_weather_kp_record_count ∧
    (0 : ℝ) < raw_S (get_domain_params "fusion") := by
  refine ⟨
    by unfold space_weather_kp_record_count; decide,
    by unfold space_weather_ap_record_count; decide,
    by unfold space_weather_stability_match_count; decide,
    by unfold space_weather_D_eff; decide,
    space_weather_stability_match_le_total,
    fusion_raw_S_positive
  ⟩

end

end FSOT.Formal
