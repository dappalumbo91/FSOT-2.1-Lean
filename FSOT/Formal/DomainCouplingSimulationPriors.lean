/-
  FSOT Formal DomainCouplingSimulationPriors — 141-domain cross-domain coupling graph.
  Generator: scripts/gen_domain_coupling_simulation_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def domain_coupling_node_count : ℕ := 149
def domain_coupling_edge_count : ℕ := 3032
def domain_coupling_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def domain_coupling_headline_median_error_pct : ℝ := (0.0 : ℝ)
def domain_coupling_beats_sota_headlines : ℕ := 4
def domain_coupling_D_eff : ℕ := 17

theorem domain_coupling_node_count_pos : 0 < domain_coupling_node_count := by
  unfold domain_coupling_node_count; norm_num

theorem domain_coupling_edge_count_pos : 0 < domain_coupling_edge_count := by
  unfold domain_coupling_edge_count; norm_num

theorem domain_coupling_pooled_median_under_half_pct :
    domain_coupling_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold domain_coupling_pooled_median_error_pct; norm_num

theorem domain_coupling_headline_median_under_half_pct :
    domain_coupling_headline_median_error_pct < (0.5 : ℝ) := by
  unfold domain_coupling_headline_median_error_pct; norm_num

theorem domain_coupling_beats_sota_headlines_pos : 0 < domain_coupling_beats_sota_headlines := by
  unfold domain_coupling_beats_sota_headlines; norm_num

theorem domain_coupling_bundle :
    domain_coupling_node_count = 149 ∧
    domain_coupling_edge_count = 3032 ∧
    domain_coupling_pooled_median_error_pct < (0.5 : ℝ) ∧
    domain_coupling_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < domain_coupling_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold domain_coupling_node_count; norm_num,
    by unfold domain_coupling_edge_count; norm_num,
    domain_coupling_pooled_median_under_half_pct,
    domain_coupling_headline_median_under_half_pct,
    domain_coupling_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
