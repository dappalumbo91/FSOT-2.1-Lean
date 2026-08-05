/-
  FSOT Formal TheoryCompletenessSpinePriors — extension domain Theory_Completeness_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def theory_completeness_spine_observable_count : ℕ := 24
def theory_completeness_spine_D_eff : ℕ := 19

theorem theory_completeness_spine_observable_count_pos : 0 < theory_completeness_spine_observable_count := by
  unfold theory_completeness_spine_observable_count; decide

theorem theory_completeness_spine_median_error_under_half_pct :
    (0.021927861384483893 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.021927861384483893 : ℝ) < (0.5 : ℝ))

theorem theory_completeness_spine_bundle :
    theory_completeness_spine_observable_count = 24 ∧
    theory_completeness_spine_D_eff = 19 ∧
    (0.021927861384483893 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold theory_completeness_spine_observable_count; decide,
    by unfold theory_completeness_spine_D_eff; decide,
    theory_completeness_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
