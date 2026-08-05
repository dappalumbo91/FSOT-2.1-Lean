/-
  FSOT Formal NcbiGenePublicPriors — Tier 81 credential-free public (NCBI_Gene_Public_Panel).
  Generator: scripts/gen_tier81_public_verifiable_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def ncbi_gene_public_observable_count : ℕ := 48
def ncbi_gene_public_median_error_pct : ℝ := (0.025571999999999998 : ℝ)
def ncbi_gene_public_D_eff : ℕ := 12

theorem ncbi_gene_public_observable_count_pos : 0 < ncbi_gene_public_observable_count := by
  unfold ncbi_gene_public_observable_count; decide

theorem ncbi_gene_public_median_error_under_five_pct :
    ncbi_gene_public_median_error_pct < (5 : ℝ) := by
  unfold ncbi_gene_public_median_error_pct
  exact (by norm_num : (0.025571999999999998  : ℝ) < (5 : ℝ))

theorem ncbi_gene_public_bundle :
    ncbi_gene_public_observable_count = 48 ∧
    ncbi_gene_public_D_eff = 12 ∧
    ncbi_gene_public_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold ncbi_gene_public_observable_count; decide,
    by unfold ncbi_gene_public_D_eff; decide,
    ncbi_gene_public_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
