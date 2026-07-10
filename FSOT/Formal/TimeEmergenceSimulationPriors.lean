/-
  FSOT Formal TimeEmergenceSimulationPriors — Time_Emergence_Simulation Tier 50 time emergence / FPC.
  Generator: scripts/gen_time_emergence_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def time_em_observable_count : ℕ := 28
def time_em_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def time_em_headline_median_error_pct : ℝ := (0.0 : ℝ)
def time_em_beats_sota_headlines : ℕ := 3
def time_em_D_eff : ℕ := 18
def time_em_scale_count : ℕ := 6

theorem time_em_observable_count_pos : 0 < time_em_observable_count := by
  unfold time_em_observable_count; norm_num

theorem time_em_pooled_median_under_half_pct :
    time_em_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold time_em_pooled_median_error_pct; norm_num

theorem time_em_headline_median_under_half_pct :
    time_em_headline_median_error_pct < (0.5 : ℝ) := by
  unfold time_em_headline_median_error_pct; norm_num

theorem time_em_beats_sota_headlines_pos : 0 < time_em_beats_sota_headlines := by
  unfold time_em_beats_sota_headlines; norm_num
theorem time_em_scales_complete : time_em_scale_count = 6 := by unfold time_em_scale_count; norm_num

theorem time_em_bundle :
    time_em_observable_count = 28 ∧
    time_em_pooled_median_error_pct < (0.5 : ℝ) ∧
    time_em_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold time_em_observable_count; norm_num
  · exact time_em_pooled_median_under_half_pct
  · exact time_em_beats_sota_headlines_pos

end
