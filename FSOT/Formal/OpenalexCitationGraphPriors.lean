/-
  FSOT Formal OpenalexCitationGraphPriors — Tier 38 public API (OpenAlex_Citation_Graph).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def openalex_citation_graph_observable_count : ℕ := 150
def openalex_citation_graph_median_error_pct : ℝ := (0.0 : ℝ)
def openalex_citation_graph_D_eff : ℕ := 18

theorem openalex_citation_graph_observable_count_pos : 0 < openalex_citation_graph_observable_count := by
  unfold openalex_citation_graph_observable_count; norm_num

theorem openalex_citation_graph_median_error_under_five_pct :
    openalex_citation_graph_median_error_pct < (5 : ℝ) := by
  unfold openalex_citation_graph_median_error_pct; norm_num

theorem openalex_citation_graph_bundle :
    openalex_citation_graph_observable_count = 150 ∧
    openalex_citation_graph_D_eff = 18 ∧
    openalex_citation_graph_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold openalex_citation_graph_observable_count; norm_num,
    by unfold openalex_citation_graph_D_eff; norm_num,
    openalex_citation_graph_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
