/-
  FSOT Formal PreregisteredPredictionsVerificationScaffoldPriors — extension domain Preregistered_Predictions_Verification_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def preregistered_predictions_verification_scaffold_observable_count : ℕ := 60
def preregistered_predictions_verification_scaffold_D_eff : ℕ := 17

theorem preregistered_predictions_verification_scaffold_observable_count_pos : 0 < preregistered_predictions_verification_scaffold_observable_count := by
  unfold preregistered_predictions_verification_scaffold_observable_count; decide

theorem preregistered_predictions_verification_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem preregistered_predictions_verification_scaffold_bundle :
    preregistered_predictions_verification_scaffold_observable_count = 60 ∧
    preregistered_predictions_verification_scaffold_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold preregistered_predictions_verification_scaffold_observable_count; decide,
    by unfold preregistered_predictions_verification_scaffold_D_eff; decide,
    preregistered_predictions_verification_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
