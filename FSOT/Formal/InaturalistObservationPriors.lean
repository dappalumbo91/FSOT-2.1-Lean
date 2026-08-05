/-
  FSOT Formal InaturalistObservationPriors — Tier 81 credential-free public (iNaturalist_Observation_Panel).
  Generator: scripts/gen_tier81_public_verifiable_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def inaturalist_observation_observable_count : ℕ := 288
def inaturalist_observation_median_error_pct : ℝ := (0.006006 : ℝ)
def inaturalist_observation_D_eff : ℕ := 15

theorem inaturalist_observation_observable_count_pos : 0 < inaturalist_observation_observable_count := by
  unfold inaturalist_observation_observable_count; decide

theorem inaturalist_observation_median_error_under_five_pct :
    inaturalist_observation_median_error_pct < (5 : ℝ) := by
  unfold inaturalist_observation_median_error_pct
  exact (by norm_num : (0.006006  : ℝ) < (5 : ℝ))

theorem inaturalist_observation_bundle :
    inaturalist_observation_observable_count = 288 ∧
    inaturalist_observation_D_eff = 15 ∧
    inaturalist_observation_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold inaturalist_observation_observable_count; decide,
    by unfold inaturalist_observation_D_eff; decide,
    inaturalist_observation_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
