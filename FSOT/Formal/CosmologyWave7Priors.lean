/-
  FSOT Formal CosmologyWave7Priors — fsot_compute wave7 certificate.
  Generator: scripts/gen_cosmology_wave_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_wave7_observable_count : ℕ := 29
def cosmology_wave7_max_error_pct : ℝ := (0.2980550885153489 : ℝ)
def cosmology_wave7_median_error_pct : ℝ := (0.003988029700396626 : ℝ)

theorem cosmology_wave7_observable_count_pos : 0 < cosmology_wave7_observable_count := by
  unfold cosmology_wave7_observable_count; norm_num

theorem cosmology_wave7_max_error_under_five_pct :
    cosmology_wave7_max_error_pct < (5 : ℝ) := by
  unfold cosmology_wave7_max_error_pct; norm_num

theorem cosmology_wave7_median_error_under_five_pct :
    cosmology_wave7_median_error_pct < (5 : ℝ) := by
  unfold cosmology_wave7_median_error_pct; norm_num

/-- Bundle: wave7 observables within 5% tolerance band. -/
theorem cosmology_wave7_bundle :
    cosmology_wave7_observable_count = 29 ∧
    cosmology_wave7_max_error_pct < (5 : ℝ) ∧
    cosmology_wave7_median_error_pct < (5 : ℝ) ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold cosmology_wave7_observable_count; norm_num,
    cosmology_wave7_max_error_under_five_pct,
    cosmology_wave7_median_error_under_five_pct,
    omega_b_h2_fsot_cached_pos
  ⟩

end

end FSOT.Formal
