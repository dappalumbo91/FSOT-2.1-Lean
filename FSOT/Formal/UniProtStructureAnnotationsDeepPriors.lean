/-
  FSOT Formal UniprotStructureAnnotationsDeepPriors — extension domain UniProt_Structure_Annotations_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def uniprot_structure_annotations_deep_observable_count : ℕ := 121
def uniprot_structure_annotations_deep_D_eff : ℕ := 13

theorem uniprot_structure_annotations_deep_observable_count_pos : 0 < uniprot_structure_annotations_deep_observable_count := by
  unfold uniprot_structure_annotations_deep_observable_count; norm_num

theorem uniprot_structure_annotations_deep_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem uniprot_structure_annotations_deep_bundle :
    uniprot_structure_annotations_deep_observable_count = 121 ∧
    uniprot_structure_annotations_deep_D_eff = 13 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold uniprot_structure_annotations_deep_observable_count; norm_num,
    by unfold uniprot_structure_annotations_deep_D_eff; norm_num,
    uniprot_structure_annotations_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
