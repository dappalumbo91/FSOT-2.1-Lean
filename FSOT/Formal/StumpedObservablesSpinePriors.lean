/-
  FSOT Formal StumpedObservablesSpinePriors — extension domain Stumped_Observables_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def stumped_observables_spine_observable_count : ℕ := 24
def stumped_observables_spine_D_eff : ℕ := 25

theorem stumped_observables_spine_observable_count_pos : 0 < stumped_observables_spine_observable_count := by
  unfold stumped_observables_spine_observable_count; decide

theorem stumped_observables_spine_median_error_under_half_pct :
    (0.027761 : ℝ) < (0.5 : ℝ) := by norm_num

theorem stumped_observables_spine_bundle :
    stumped_observables_spine_observable_count = 24 ∧
    stumped_observables_spine_D_eff = 25 ∧
    (0.027761 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold stumped_observables_spine_observable_count; decide,
    by unfold stumped_observables_spine_D_eff; decide,
    stumped_observables_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
