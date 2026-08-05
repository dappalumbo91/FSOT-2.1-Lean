/-
  FSOT Formal OpenalexCitationDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def openalex_citation_depth_open_observable_count : ℕ := 150
def openalex_citation_depth_open_pooled_median_error_pct : ℝ := (0.008863 : ℝ)
def openalex_citation_depth_open_headline_median_error_pct : ℝ := (0.031506 : ℝ)
def openalex_citation_depth_open_D_eff : ℕ := 12

theorem openalex_citation_depth_open_observable_count_pos : 0 < openalex_citation_depth_open_observable_count := by
  unfold openalex_citation_depth_open_observable_count; decide

theorem openalex_citation_depth_open_pooled_median_under_half_pct :
    openalex_citation_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold openalex_citation_depth_open_pooled_median_error_pct
  exact (by norm_num : (0.008863  : ℝ) < 0.5)

theorem openalex_citation_depth_open_headline_median_under_half_pct :
    openalex_citation_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold openalex_citation_depth_open_headline_median_error_pct
  exact (by norm_num : (0.031506  : ℝ) < 0.5)

theorem openalex_citation_depth_open_bundle :
    openalex_citation_depth_open_observable_count = 150 ∧
    openalex_citation_depth_open_D_eff = 12 ∧
    openalex_citation_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold openalex_citation_depth_open_observable_count; decide
  · unfold openalex_citation_depth_open_D_eff; decide
  · exact openalex_citation_depth_open_pooled_median_under_half_pct

end
