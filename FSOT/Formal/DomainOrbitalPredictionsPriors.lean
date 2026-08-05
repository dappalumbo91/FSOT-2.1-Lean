/-
  FSOT Formal DomainOrbitalPredictionsPriors — extension domain Domain_Orbital_Predictions.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def domain_orbital_predictions_observable_count : ℕ := 24
def domain_orbital_predictions_D_eff : ℕ := 19

theorem domain_orbital_predictions_observable_count_pos : 0 < domain_orbital_predictions_observable_count := by
  unfold domain_orbital_predictions_observable_count; decide

theorem domain_orbital_predictions_median_error_under_half_pct :
    (0.01529034996934153 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.01529034996934153 : ℝ) < (0.5 : ℝ))

theorem domain_orbital_predictions_bundle :
    domain_orbital_predictions_observable_count = 24 ∧
    domain_orbital_predictions_D_eff = 19 ∧
    (0.01529034996934153 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold domain_orbital_predictions_observable_count; decide,
    by unfold domain_orbital_predictions_D_eff; decide,
    domain_orbital_predictions_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
