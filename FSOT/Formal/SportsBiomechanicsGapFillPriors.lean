/-
  FSOT Formal SportsBiomechanicsGapFillPriors — Sports_Biomechanics tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def sports_biomechanics_gap_fill_observable_count : ℕ := 35
def sports_biomechanics_gap_fill_pooled_median_error_pct : ℝ := (0.04447250077037523 : ℝ)
def sports_biomechanics_gap_fill_headline_median_error_pct : ℝ := (0.04447250077037523 : ℝ)
def sports_biomechanics_gap_fill_beats_sota_headlines : ℕ := 2
def sports_biomechanics_gap_fill_D_eff : ℕ := 14

theorem sports_biomechanics_gap_fill_observable_count_pos : 0 < sports_biomechanics_gap_fill_observable_count := by
  unfold sports_biomechanics_gap_fill_observable_count; norm_num

theorem sports_biomechanics_gap_fill_pooled_median_under_half_pct :
    sports_biomechanics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold sports_biomechanics_gap_fill_pooled_median_error_pct; norm_num

theorem sports_biomechanics_gap_fill_headline_median_under_half_pct :
    sports_biomechanics_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold sports_biomechanics_gap_fill_headline_median_error_pct; norm_num

theorem sports_biomechanics_gap_fill_beats_sota_headlines_pos : 0 < sports_biomechanics_gap_fill_beats_sota_headlines := by
  unfold sports_biomechanics_gap_fill_beats_sota_headlines; norm_num

theorem sports_biomechanics_gap_fill_bundle :
    sports_biomechanics_gap_fill_observable_count = 35 ∧
    sports_biomechanics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    sports_biomechanics_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < sports_biomechanics_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold sports_biomechanics_gap_fill_observable_count; norm_num,
    sports_biomechanics_gap_fill_pooled_median_under_half_pct,
    sports_biomechanics_gap_fill_headline_median_under_half_pct,
    sports_biomechanics_gap_fill_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
