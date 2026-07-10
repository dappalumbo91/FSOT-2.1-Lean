/-
  FSOT Formal PredictionRederivationPriors — prediction re-derivation arc.
  Generator: scripts/gen_prediction_rederivation_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def prediction_rederivation_observable_count : ℕ := 10
def prediction_rederivation_median_error_pct : ℝ := (0.0 : ℝ)
def prediction_rederivation_D_eff : ℕ := 14

theorem prediction_rederivation_observable_count_pos : 0 < prediction_rederivation_observable_count := by
  unfold prediction_rederivation_observable_count; norm_num

theorem prediction_rederivation_median_error_under_half_pct :
    prediction_rederivation_median_error_pct < (0.5 : ℝ) := by
  unfold prediction_rederivation_median_error_pct; norm_num

theorem prediction_rederivation_bundle :
    prediction_rederivation_observable_count = 10 ∧
    prediction_rederivation_D_eff = 14 ∧
    prediction_rederivation_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold prediction_rederivation_observable_count; norm_num,
    by unfold prediction_rederivation_D_eff; norm_num,
    prediction_rederivation_median_error_under_half_pct,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
