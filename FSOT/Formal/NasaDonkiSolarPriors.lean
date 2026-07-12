/-
  FSOT Formal NasaDonkiSolarPriors — Tier 80 government open data (NASA_DONKI_Solar_Panel).
  Generator: scripts/gen_tier80_government_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def nasa_donki_solar_observable_count : ℕ := 397
def nasa_donki_solar_median_error_pct : ℝ := (0.020755 : ℝ)
def nasa_donki_solar_D_eff : ℕ := 14

theorem nasa_donki_solar_observable_count_pos : 0 < nasa_donki_solar_observable_count := by
  unfold nasa_donki_solar_observable_count; norm_num

theorem nasa_donki_solar_median_error_under_five_pct :
    nasa_donki_solar_median_error_pct < (5 : ℝ) := by
  unfold nasa_donki_solar_median_error_pct; norm_num

theorem nasa_donki_solar_bundle :
    nasa_donki_solar_observable_count = 397 ∧
    nasa_donki_solar_D_eff = 14 ∧
    nasa_donki_solar_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "fusion") > 0 := by
  refine ⟨
    by unfold nasa_donki_solar_observable_count; norm_num,
    by unfold nasa_donki_solar_D_eff; norm_num,
    nasa_donki_solar_median_error_under_five_pct,
    fusion_raw_S_positive
  ⟩

end

end FSOT.Formal
