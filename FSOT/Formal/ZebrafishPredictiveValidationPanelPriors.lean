/-
  FSOT Formal ZebrafishPredictiveValidationPanelPriors — Tier 95 Zebrahub developmental (Zebrafish_Predictive_Validation_Panel).
  Generator: scripts/gen_tier95_zebrahub_development_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def zebrafish_predictive_validation_observable_count : ℕ := 20
def zebrafish_predictive_validation_median_error_pct : ℝ := (0.3579695 : ℝ)
def zebrafish_predictive_validation_D_eff : ℕ := 24

theorem zebrafish_predictive_validation_observable_count_pos : 0 < zebrafish_predictive_validation_observable_count := by
  unfold zebrafish_predictive_validation_observable_count; decide

theorem zebrafish_predictive_validation_median_error_under_five_pct :
    zebrafish_predictive_validation_median_error_pct < (5 : ℝ) := by
  unfold zebrafish_predictive_validation_median_error_pct
  exact (by norm_num : (0.3579695  : ℝ) < (5 : ℝ))

theorem zebrafish_predictive_validation_bundle :
    zebrafish_predictive_validation_observable_count = 20 ∧
    zebrafish_predictive_validation_D_eff = 24 ∧
    zebrafish_predictive_validation_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold zebrafish_predictive_validation_observable_count; decide,
    by unfold zebrafish_predictive_validation_D_eff; decide,
    zebrafish_predictive_validation_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
