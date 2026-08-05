/-
  FSOT Formal AgricultureAgroecologyGapFillPriors — Agriculture_Agroecology tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def agriculture_agroecology_gap_fill_observable_count : ℕ := 276
def agriculture_agroecology_gap_fill_pooled_median_error_pct : ℝ := (0.018019024892929635 : ℝ)
def agriculture_agroecology_gap_fill_headline_median_error_pct : ℝ := (0.018019024892929635 : ℝ)
def agriculture_agroecology_gap_fill_beats_sota_headlines : ℕ := 2
def agriculture_agroecology_gap_fill_D_eff : ℕ := 16

theorem agriculture_agroecology_gap_fill_observable_count_pos : 0 < agriculture_agroecology_gap_fill_observable_count := by
  unfold agriculture_agroecology_gap_fill_observable_count; decide

theorem agriculture_agroecology_gap_fill_pooled_median_under_half_pct :
    agriculture_agroecology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold agriculture_agroecology_gap_fill_pooled_median_error_pct
  exact (by norm_num : (0.018019024892929635  : ℝ) < 0.5)

theorem agriculture_agroecology_gap_fill_headline_median_under_half_pct :
    agriculture_agroecology_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold agriculture_agroecology_gap_fill_headline_median_error_pct
  exact (by norm_num : (0.018019024892929635  : ℝ) < 0.5)

theorem agriculture_agroecology_gap_fill_beats_sota_headlines_pos : 0 < agriculture_agroecology_gap_fill_beats_sota_headlines := by
  unfold agriculture_agroecology_gap_fill_beats_sota_headlines; decide

theorem agriculture_agroecology_gap_fill_bundle :
    agriculture_agroecology_gap_fill_observable_count = 276 ∧
    agriculture_agroecology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    agriculture_agroecology_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < agriculture_agroecology_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold agriculture_agroecology_gap_fill_observable_count; decide,
    agriculture_agroecology_gap_fill_pooled_median_under_half_pct,
    agriculture_agroecology_gap_fill_headline_median_under_half_pct,
    agriculture_agroecology_gap_fill_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
