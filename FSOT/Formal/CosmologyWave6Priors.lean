/-
  FSOT Formal CosmologyWave6Priors — fsot_compute wave6 certificate.
  Generator: scripts/gen_cosmology_wave_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_wave6_observable_count : ℕ := 22
def cosmology_wave6_max_error_pct : ℝ := (0.031298130508454446 : ℝ)
def cosmology_wave6_median_error_pct : ℝ := (0.0003441841587202251 : ℝ)

theorem cosmology_wave6_observable_count_pos : 0 < cosmology_wave6_observable_count := by
  unfold cosmology_wave6_observable_count; decide

theorem cosmology_wave6_max_error_under_half_pct :
    cosmology_wave6_max_error_pct < (0.5 : ℝ) := by
  unfold cosmology_wave6_max_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem cosmology_wave6_median_error_under_half_pct :
    cosmology_wave6_median_error_pct < (0.5 : ℝ) := by
  unfold cosmology_wave6_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

/-- Bundle: wave6 observables within 5% tolerance band. -/
theorem cosmology_wave6_bundle :
    cosmology_wave6_observable_count = 22 ∧
    cosmology_wave6_max_error_pct < (0.5 : ℝ) ∧
    cosmology_wave6_median_error_pct < (0.5 : ℝ) ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold cosmology_wave6_observable_count; decide,
    cosmology_wave6_max_error_under_half_pct,
    cosmology_wave6_median_error_under_half_pct,
    omega_b_h2_fsot_cached_pos
  ⟩

end

end FSOT.Formal
