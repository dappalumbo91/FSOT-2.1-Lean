/-
  FSOT Formal UniprotProteinAnnotationsPriors — Tier 38 public API (UniProt_Protein_Annotations).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def uniprot_protein_annotations_observable_count : ℕ := 62
def uniprot_protein_annotations_median_error_pct : ℝ := (0.0 : ℝ)
def uniprot_protein_annotations_D_eff : ℕ := 12

theorem uniprot_protein_annotations_observable_count_pos : 0 < uniprot_protein_annotations_observable_count := by
  unfold uniprot_protein_annotations_observable_count; norm_num

theorem uniprot_protein_annotations_median_error_under_five_pct :
    uniprot_protein_annotations_median_error_pct < (5 : ℝ) := by
  unfold uniprot_protein_annotations_median_error_pct; norm_num

theorem uniprot_protein_annotations_bundle :
    uniprot_protein_annotations_observable_count = 62 ∧
    uniprot_protein_annotations_D_eff = 12 ∧
    uniprot_protein_annotations_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold uniprot_protein_annotations_observable_count; norm_num,
    by unfold uniprot_protein_annotations_D_eff; norm_num,
    uniprot_protein_annotations_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
