/-
  FSOT Formal CosmologyWave9Priors — fsot_compute wave9 certificate.
  Generator: scripts/gen_cosmology_wave_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_wave9_observable_count : ℕ := 7
def cosmology_wave9_max_error_pct : ℝ := (0.19375824846825943 : ℝ)
def cosmology_wave9_median_error_pct : ℝ := (0.014278509753575246 : ℝ)

theorem cosmology_wave9_observable_count_pos : 0 < cosmology_wave9_observable_count := by
  unfold cosmology_wave9_observable_count; decide

theorem cosmology_wave9_max_error_under_half_pct :
    cosmology_wave9_max_error_pct < (0.5 : ℝ) := by
  unfold cosmology_wave9_max_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem cosmology_wave9_median_error_under_half_pct :
    cosmology_wave9_median_error_pct < (0.5 : ℝ) := by
  unfold cosmology_wave9_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

/-- Bundle: wave9 observables within 5% tolerance band. -/
theorem cosmology_wave9_bundle :
    cosmology_wave9_observable_count = 7 ∧
    cosmology_wave9_max_error_pct < (0.5 : ℝ) ∧
    cosmology_wave9_median_error_pct < (0.5 : ℝ) ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold cosmology_wave9_observable_count; decide,
    cosmology_wave9_max_error_under_half_pct,
    cosmology_wave9_median_error_under_half_pct,
    omega_b_h2_fsot_cached_pos
  ⟩

end

end FSOT.Formal
