/-
  FSOT Formal NoaaNdbcBuoyPriors — Tier 81 credential-free public (NOAA_NDBC_Buoy_Panel).
  Generator: scripts/gen_tier81_public_verifiable_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def noaa_ndbc_buoy_observable_count : ℕ := 596
def noaa_ndbc_buoy_median_error_pct : ℝ := (0.028287 : ℝ)
def noaa_ndbc_buoy_D_eff : ℕ := 17

theorem noaa_ndbc_buoy_observable_count_pos : 0 < noaa_ndbc_buoy_observable_count := by
  unfold noaa_ndbc_buoy_observable_count; norm_num

theorem noaa_ndbc_buoy_median_error_under_five_pct :
    noaa_ndbc_buoy_median_error_pct < (5 : ℝ) := by
  unfold noaa_ndbc_buoy_median_error_pct; norm_num

theorem noaa_ndbc_buoy_bundle :
    noaa_ndbc_buoy_observable_count = 596 ∧
    noaa_ndbc_buoy_D_eff = 17 ∧
    noaa_ndbc_buoy_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold noaa_ndbc_buoy_observable_count; norm_num,
    by unfold noaa_ndbc_buoy_D_eff; norm_num,
    noaa_ndbc_buoy_median_error_under_five_pct,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
