/-
  FSOT Formal NoaaCoastalTidesPriors — Tier 38 public API (NOAA_Coastal_Tides).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def noaa_coastal_tides_observable_count : ℕ := 40
def noaa_coastal_tides_median_error_pct : ℝ := (0.0 : ℝ)
def noaa_coastal_tides_D_eff : ℕ := 17

theorem noaa_coastal_tides_observable_count_pos : 0 < noaa_coastal_tides_observable_count := by
  unfold noaa_coastal_tides_observable_count; norm_num

theorem noaa_coastal_tides_median_error_under_half_pct :
    noaa_coastal_tides_median_error_pct < (0.5 : ℝ) := by
  unfold noaa_coastal_tides_median_error_pct; norm_num

theorem noaa_coastal_tides_bundle :
    noaa_coastal_tides_observable_count = 40 ∧
    noaa_coastal_tides_D_eff = 17 ∧
    noaa_coastal_tides_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold noaa_coastal_tides_observable_count; norm_num,
    by unfold noaa_coastal_tides_D_eff; norm_num,
    noaa_coastal_tides_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
