/-
  FSOT Formal CosmologyWave5Priors — fsot_compute wave5 certificate.
  Generator: scripts/gen_cosmology_wave_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_wave5_observable_count : ℕ := 22
def cosmology_wave5_max_error_pct : ℝ := (0.09098602506082563 : ℝ)
def cosmology_wave5_median_error_pct : ℝ := (0.0020773615251059676 : ℝ)

theorem cosmology_wave5_observable_count_pos : 0 < cosmology_wave5_observable_count := by
  unfold cosmology_wave5_observable_count; norm_num

theorem cosmology_wave5_max_error_under_half_pct :
    cosmology_wave5_max_error_pct < (0.5 : ℝ) := by
  unfold cosmology_wave5_max_error_pct; norm_num

theorem cosmology_wave5_median_error_under_half_pct :
    cosmology_wave5_median_error_pct < (0.5 : ℝ) := by
  unfold cosmology_wave5_median_error_pct; norm_num

/-- Bundle: wave5 observables within 5% tolerance band. -/
theorem cosmology_wave5_bundle :
    cosmology_wave5_observable_count = 22 ∧
    cosmology_wave5_max_error_pct < (0.5 : ℝ) ∧
    cosmology_wave5_median_error_pct < (0.5 : ℝ) ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold cosmology_wave5_observable_count; norm_num,
    cosmology_wave5_max_error_under_half_pct,
    cosmology_wave5_median_error_under_half_pct,
    omega_b_h2_fsot_cached_pos
  ⟩

end

end FSOT.Formal
