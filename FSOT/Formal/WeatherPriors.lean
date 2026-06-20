/-
  FSOT Formal WeatherPriors — atmospheric scalar simulation certificates.

  Source: weather/fsot_weather_sim_log.json
  Generator: scripts/gen_weather_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def weather_hour_count : ℕ := 24
def weather_D_eff : ℕ := 15
def weather_S_min : ℝ := (0.364542 : ℝ)
def weather_S_mean : ℝ := (0.48326775000000016 : ℝ)

theorem weather_S_min_positive : (0 : ℝ) < weather_S_min := by
  unfold weather_S_min; norm_num

theorem weather_hour_count_pos : 0 < weather_hour_count := by
  unfold weather_hour_count; norm_num

/-- Bundle: 24-hour weather sim at D_eff=15 with positive S (medical-domain sign proxy). -/
theorem weather_priors_bundle :
    weather_hour_count = 24 ∧
    weather_D_eff = 15 ∧
    weather_S_min = (0.364542 : ℝ) ∧
    weather_S_mean = (0.48326775000000016 : ℝ) ∧
    (0 : ℝ) < weather_S_min ∧
    (0 : ℝ) < raw_S (get_domain_params "medical") := by
  refine ⟨
    by unfold weather_hour_count; norm_num,
    by unfold weather_D_eff; norm_num,
    by unfold weather_S_min; norm_num,
    by unfold weather_S_mean; norm_num,
    weather_S_min_positive,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
