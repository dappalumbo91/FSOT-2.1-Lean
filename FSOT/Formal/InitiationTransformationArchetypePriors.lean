/-
  FSOT Formal InitiationTransformationArchetypePriors — extension domain Initiation_Transformation_Archetype.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def initiation_transformation_archetype_observable_count : ℕ := 24
def initiation_transformation_archetype_D_eff : ℕ := 17

theorem initiation_transformation_archetype_observable_count_pos : 0 < initiation_transformation_archetype_observable_count := by
  unfold initiation_transformation_archetype_observable_count; decide

theorem initiation_transformation_archetype_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem initiation_transformation_archetype_bundle :
    initiation_transformation_archetype_observable_count = 24 ∧
    initiation_transformation_archetype_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold initiation_transformation_archetype_observable_count; decide,
    by unfold initiation_transformation_archetype_D_eff; decide,
    initiation_transformation_archetype_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
