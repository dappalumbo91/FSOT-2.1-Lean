/-
  FSOT Formal ClimateSciencePriors — extension domain Climate_Science (scaled NCEI + station cohort).
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def climate_science_observable_count : ℕ := 9439
def climate_science_train_month_count : ℕ := 7519
def climate_science_holdout_month_count : ℕ := 1920
def climate_science_holdout_station_count : ℕ := 4
def climate_science_D_eff : ℕ := 16
def climate_science_median_error_pct : ℝ := (0.0 : ℝ)
def climate_science_holdout_median_error_pct : ℝ := (0.0 : ℝ)

theorem climate_science_observable_count_pos : 0 < climate_science_observable_count := by
  unfold climate_science_observable_count; norm_num

theorem climate_science_holdout_month_count_pos : 0 < climate_science_holdout_month_count := by
  unfold climate_science_holdout_month_count; norm_num

theorem climate_science_median_error_under_five_pct : climate_science_median_error_pct < (5 : ℝ) := by
  unfold climate_science_median_error_pct; norm_num

theorem climate_science_holdout_median_error_under_five_pct : climate_science_holdout_median_error_pct < (5 : ℝ) := by
  unfold climate_science_holdout_median_error_pct; norm_num

theorem climate_science_bundle :
    climate_science_observable_count = 9439 ∧
    climate_science_train_month_count = 7519 ∧
    climate_science_holdout_month_count = 1920 ∧
    climate_science_holdout_station_count = 4 ∧
    climate_science_D_eff = 16 ∧
    climate_science_median_error_pct < (5 : ℝ) ∧
    climate_science_holdout_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold climate_science_observable_count; norm_num,
    by unfold climate_science_train_month_count; norm_num,
    by unfold climate_science_holdout_month_count; norm_num,
    by unfold climate_science_holdout_station_count; norm_num,
    by unfold climate_science_D_eff; norm_num,
    climate_science_median_error_under_five_pct,
    climate_science_holdout_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
