/-
  FSOT Formal GbifTaxonDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gbif_taxon_depth_open_observable_count : ℕ := 203
def gbif_taxon_depth_open_pooled_median_error_pct : ℝ := (0.006006 : ℝ)
def gbif_taxon_depth_open_headline_median_error_pct : ℝ := (0.006006 : ℝ)
def gbif_taxon_depth_open_D_eff : ℕ := 14

theorem gbif_taxon_depth_open_observable_count_pos : 0 < gbif_taxon_depth_open_observable_count := by
  unfold gbif_taxon_depth_open_observable_count; norm_num

theorem gbif_taxon_depth_open_pooled_median_under_half_pct :
    gbif_taxon_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold gbif_taxon_depth_open_pooled_median_error_pct; norm_num

theorem gbif_taxon_depth_open_headline_median_under_half_pct :
    gbif_taxon_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold gbif_taxon_depth_open_headline_median_error_pct; norm_num

theorem gbif_taxon_depth_open_bundle :
    gbif_taxon_depth_open_observable_count = 203 ∧
    gbif_taxon_depth_open_D_eff = 14 ∧
    gbif_taxon_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold gbif_taxon_depth_open_observable_count; norm_num
  · unfold gbif_taxon_depth_open_D_eff; norm_num
  · exact gbif_taxon_depth_open_pooled_median_under_half_pct

end
