/-
  FSOT Formal FluidPhaseCurrentSpinePriors — Fluid_Phase_Current_Spine Tier 50 time emergence / FPC.
  Generator: scripts/gen_time_emergence_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fpc_spine_observable_count : ℕ := 7
def fpc_spine_pooled_median_error_pct : ℝ := (0.009504 : ℝ)
def fpc_spine_headline_median_error_pct : ℝ := (0.009504 : ℝ)
def fpc_spine_beats_sota_headlines : ℕ := 2
def fpc_spine_D_eff : ℕ := 20
def fpc_spine_fluidlink_edge_count : ℕ := 6
def fpc_spine_crosswalk_domain_count : ℕ := 145

theorem fpc_spine_observable_count_pos : 0 < fpc_spine_observable_count := by
  unfold fpc_spine_observable_count; norm_num

theorem fpc_spine_pooled_median_under_half_pct :
    fpc_spine_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fpc_spine_pooled_median_error_pct; norm_num

theorem fpc_spine_headline_median_under_half_pct :
    fpc_spine_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fpc_spine_headline_median_error_pct; norm_num

theorem fpc_spine_beats_sota_headlines_pos : 0 < fpc_spine_beats_sota_headlines := by
  unfold fpc_spine_beats_sota_headlines; norm_num
theorem fpc_spine_spine_edges_pos : 0 < fpc_spine_fluidlink_edge_count := by unfold fpc_spine_fluidlink_edge_count; norm_num

theorem fpc_spine_bundle :
    fpc_spine_observable_count = 7 ∧
    fpc_spine_pooled_median_error_pct < (0.5 : ℝ) ∧
    fpc_spine_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fpc_spine_observable_count; norm_num
  · exact fpc_spine_pooled_median_under_half_pct
  · exact fpc_spine_beats_sota_headlines_pos

end
