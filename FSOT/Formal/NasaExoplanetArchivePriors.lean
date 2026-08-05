/-
  FSOT Formal NasaExoplanetArchivePriors — Tier 38 public API (NASA_Exoplanet_Archive).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def nasa_exoplanet_archive_observable_count : ℕ := 158
def nasa_exoplanet_archive_median_error_pct : ℝ := (0.023015 : ℝ)
def nasa_exoplanet_archive_D_eff : ℕ := 21

theorem nasa_exoplanet_archive_observable_count_pos : 0 < nasa_exoplanet_archive_observable_count := by
  unfold nasa_exoplanet_archive_observable_count; decide

theorem nasa_exoplanet_archive_median_error_under_five_pct :
    nasa_exoplanet_archive_median_error_pct < (5 : ℝ) := by
  unfold nasa_exoplanet_archive_median_error_pct
  exact (by norm_num : (0.023015  : ℝ) < (5 : ℝ))

theorem nasa_exoplanet_archive_bundle :
    nasa_exoplanet_archive_observable_count = 158 ∧
    nasa_exoplanet_archive_D_eff = 21 ∧
    nasa_exoplanet_archive_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold nasa_exoplanet_archive_observable_count; decide,
    by unfold nasa_exoplanet_archive_D_eff; decide,
    nasa_exoplanet_archive_median_error_under_five_pct,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
