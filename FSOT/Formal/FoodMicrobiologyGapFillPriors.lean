/-
  FSOT Formal FoodMicrobiologyGapFillPriors — Food_Microbiology tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def food_microbiology_gap_fill_observable_count : ℕ := 30
def food_microbiology_gap_fill_pooled_median_error_pct : ℝ := (0.04447250077037743 : ℝ)
def food_microbiology_gap_fill_headline_median_error_pct : ℝ := (0.04447250077037743 : ℝ)
def food_microbiology_gap_fill_beats_sota_headlines : ℕ := 2
def food_microbiology_gap_fill_D_eff : ℕ := 14

theorem food_microbiology_gap_fill_observable_count_pos : 0 < food_microbiology_gap_fill_observable_count := by
  unfold food_microbiology_gap_fill_observable_count; decide

theorem food_microbiology_gap_fill_pooled_median_under_half_pct :
    food_microbiology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold food_microbiology_gap_fill_pooled_median_error_pct
  exact (by norm_num : (0.04447250077037743  : ℝ) < 0.5)

theorem food_microbiology_gap_fill_headline_median_under_half_pct :
    food_microbiology_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold food_microbiology_gap_fill_headline_median_error_pct
  exact (by norm_num : (0.04447250077037743  : ℝ) < 0.5)

theorem food_microbiology_gap_fill_beats_sota_headlines_pos : 0 < food_microbiology_gap_fill_beats_sota_headlines := by
  unfold food_microbiology_gap_fill_beats_sota_headlines; decide

theorem food_microbiology_gap_fill_bundle :
    food_microbiology_gap_fill_observable_count = 30 ∧
    food_microbiology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    food_microbiology_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < food_microbiology_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold food_microbiology_gap_fill_observable_count; decide,
    food_microbiology_gap_fill_pooled_median_under_half_pct,
    food_microbiology_gap_fill_headline_median_under_half_pct,
    food_microbiology_gap_fill_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
