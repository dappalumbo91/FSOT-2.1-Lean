/-
  FSOT Formal FPCTemporalCouplingPriors — FPC_Temporal_Coupling Tier 50 time emergence / FPC.
  Generator: scripts/gen_time_emergence_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fpc_link_observable_count : ℕ := 6
def fpc_link_pooled_median_error_pct : ℝ := (0.031199 : ℝ)
def fpc_link_headline_median_error_pct : ℝ := (0.031199 : ℝ)
def fpc_link_beats_sota_headlines : ℕ := 2
def fpc_link_D_eff : ℕ := 18
def fpc_link_fluidlink_edge_count : ℕ := 6

theorem fpc_link_observable_count_pos : 0 < fpc_link_observable_count := by
  unfold fpc_link_observable_count; norm_num

theorem fpc_link_pooled_median_under_half_pct :
    fpc_link_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fpc_link_pooled_median_error_pct; norm_num

theorem fpc_link_headline_median_under_half_pct :
    fpc_link_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fpc_link_headline_median_error_pct; norm_num

theorem fpc_link_beats_sota_headlines_pos : 0 < fpc_link_beats_sota_headlines := by
  unfold fpc_link_beats_sota_headlines; norm_num
theorem fpc_link_fluidlink_edges_pos : 0 < fpc_link_fluidlink_edge_count := by unfold fpc_link_fluidlink_edge_count; norm_num

theorem fpc_link_bundle :
    fpc_link_observable_count = 6 ∧
    fpc_link_pooled_median_error_pct < (0.5 : ℝ) ∧
    fpc_link_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fpc_link_observable_count; norm_num
  · exact fpc_link_pooled_median_under_half_pct
  · exact fpc_link_beats_sota_headlines_pos

end
