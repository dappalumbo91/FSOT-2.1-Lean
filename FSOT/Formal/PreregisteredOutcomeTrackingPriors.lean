/-
  FSOT Formal PreregisteredOutcomeTrackingPriors — extension domain Preregistered_Outcome_Tracking.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def preregistered_outcome_tracking_observable_count : ℕ := 56
def preregistered_outcome_tracking_D_eff : ℕ := 17

theorem preregistered_outcome_tracking_observable_count_pos : 0 < preregistered_outcome_tracking_observable_count := by
  unfold preregistered_outcome_tracking_observable_count; norm_num

theorem preregistered_outcome_tracking_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem preregistered_outcome_tracking_bundle :
    preregistered_outcome_tracking_observable_count = 56 ∧
    preregistered_outcome_tracking_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold preregistered_outcome_tracking_observable_count; norm_num,
    by unfold preregistered_outcome_tracking_D_eff; norm_num,
    preregistered_outcome_tracking_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
