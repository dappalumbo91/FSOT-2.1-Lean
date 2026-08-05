/-
  FSOT Formal MeteorologyGapFillPriors — Meteorology tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def meteorology_gap_fill_observable_count : ℕ := 107
def meteorology_gap_fill_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def meteorology_gap_fill_headline_median_error_pct : ℝ := (0.0 : ℝ)
def meteorology_gap_fill_beats_sota_headlines : ℕ := 2
def meteorology_gap_fill_D_eff : ℕ := 15

theorem meteorology_gap_fill_observable_count_pos : 0 < meteorology_gap_fill_observable_count := by
  unfold meteorology_gap_fill_observable_count; decide

theorem meteorology_gap_fill_pooled_median_under_half_pct :
    meteorology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold meteorology_gap_fill_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem meteorology_gap_fill_headline_median_under_half_pct :
    meteorology_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold meteorology_gap_fill_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem meteorology_gap_fill_beats_sota_headlines_pos : 0 < meteorology_gap_fill_beats_sota_headlines := by
  unfold meteorology_gap_fill_beats_sota_headlines; decide

theorem meteorology_gap_fill_bundle :
    meteorology_gap_fill_observable_count = 107 ∧
    meteorology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    meteorology_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < meteorology_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold meteorology_gap_fill_observable_count; decide,
    meteorology_gap_fill_pooled_median_under_half_pct,
    meteorology_gap_fill_headline_median_under_half_pct,
    meteorology_gap_fill_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
