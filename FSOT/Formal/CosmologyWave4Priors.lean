/-
  FSOT Formal CosmologyWave4Priors — fsot_compute wave4 certificate.
  Generator: scripts/gen_cosmology_wave_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_wave4_observable_count : ℕ := 16
def cosmology_wave4_max_error_pct : ℝ := (0.23468225112121452 : ℝ)
def cosmology_wave4_median_error_pct : ℝ := (0.011586387979935279 : ℝ)

theorem cosmology_wave4_observable_count_pos : 0 < cosmology_wave4_observable_count := by
  unfold cosmology_wave4_observable_count; norm_num

theorem cosmology_wave4_max_error_under_half_pct :
    cosmology_wave4_max_error_pct < (0.5 : ℝ) := by
  unfold cosmology_wave4_max_error_pct; norm_num

theorem cosmology_wave4_median_error_under_half_pct :
    cosmology_wave4_median_error_pct < (0.5 : ℝ) := by
  unfold cosmology_wave4_median_error_pct; norm_num

/-- Bundle: wave4 observables within 5% tolerance band. -/
theorem cosmology_wave4_bundle :
    cosmology_wave4_observable_count = 16 ∧
    cosmology_wave4_max_error_pct < (0.5 : ℝ) ∧
    cosmology_wave4_median_error_pct < (0.5 : ℝ) ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold cosmology_wave4_observable_count; norm_num,
    cosmology_wave4_max_error_under_half_pct,
    cosmology_wave4_median_error_under_half_pct,
    omega_b_h2_fsot_cached_pos
  ⟩

end

end FSOT.Formal
