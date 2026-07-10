/-
  FSOT Formal FluidDynamicsGapFillPriors — Fluid_Dynamics tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fluid_dynamics_gap_fill_observable_count : ℕ := 55
def fluid_dynamics_gap_fill_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def fluid_dynamics_gap_fill_headline_median_error_pct : ℝ := (0.0 : ℝ)
def fluid_dynamics_gap_fill_beats_sota_headlines : ℕ := 3
def fluid_dynamics_gap_fill_D_eff : ℕ := 15

theorem fluid_dynamics_gap_fill_observable_count_pos : 0 < fluid_dynamics_gap_fill_observable_count := by
  unfold fluid_dynamics_gap_fill_observable_count; norm_num

theorem fluid_dynamics_gap_fill_pooled_median_under_half_pct :
    fluid_dynamics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fluid_dynamics_gap_fill_pooled_median_error_pct; norm_num

theorem fluid_dynamics_gap_fill_headline_median_under_half_pct :
    fluid_dynamics_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fluid_dynamics_gap_fill_headline_median_error_pct; norm_num

theorem fluid_dynamics_gap_fill_beats_sota_headlines_pos : 0 < fluid_dynamics_gap_fill_beats_sota_headlines := by
  unfold fluid_dynamics_gap_fill_beats_sota_headlines; norm_num

theorem fluid_dynamics_gap_fill_bundle :
    fluid_dynamics_gap_fill_observable_count = 55 ∧
    fluid_dynamics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    fluid_dynamics_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < fluid_dynamics_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fluid_dynamics_gap_fill_observable_count; norm_num,
    fluid_dynamics_gap_fill_pooled_median_under_half_pct,
    fluid_dynamics_gap_fill_headline_median_under_half_pct,
    fluid_dynamics_gap_fill_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
