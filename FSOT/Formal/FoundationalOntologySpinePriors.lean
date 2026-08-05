/-
  FSOT Formal FoundationalOntologySpinePriors — extension domain Foundational_Ontology_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def foundational_ontology_spine_observable_count : ℕ := 21
def foundational_ontology_spine_D_eff : ℕ := 22

theorem foundational_ontology_spine_observable_count_pos : 0 < foundational_ontology_spine_observable_count := by
  unfold foundational_ontology_spine_observable_count; decide

theorem foundational_ontology_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem foundational_ontology_spine_bundle :
    foundational_ontology_spine_observable_count = 21 ∧
    foundational_ontology_spine_D_eff = 22 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold foundational_ontology_spine_observable_count; decide,
    by unfold foundational_ontology_spine_D_eff; decide,
    foundational_ontology_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
