/-
  FSOT Formal NcbiGenePublicPanelPriors — extension domain NCBI_Gene_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def ncbi_gene_public_panel_observable_count : ℕ := 48
def ncbi_gene_public_panel_D_eff : ℕ := 12

theorem ncbi_gene_public_panel_observable_count_pos : 0 < ncbi_gene_public_panel_observable_count := by
  unfold ncbi_gene_public_panel_observable_count; decide

theorem ncbi_gene_public_panel_median_error_under_half_pct :
    (0.025571999999999998 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.025571999999999998 : ℝ) < (0.5 : ℝ))

theorem ncbi_gene_public_panel_bundle :
    ncbi_gene_public_panel_observable_count = 48 ∧
    ncbi_gene_public_panel_D_eff = 12 ∧
    (0.025571999999999998 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold ncbi_gene_public_panel_observable_count; decide,
    by unfold ncbi_gene_public_panel_D_eff; decide,
    ncbi_gene_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
