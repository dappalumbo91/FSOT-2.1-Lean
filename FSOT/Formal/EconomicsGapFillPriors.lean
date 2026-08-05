/-
  FSOT Formal EconomicsGapFillPriors — Economics tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def economics_gap_fill_observable_count : ℕ := 157
def economics_gap_fill_pooled_median_error_pct : ℝ := (0.1292009041371501 : ℝ)
def economics_gap_fill_headline_median_error_pct : ℝ := (0.1292009041371501 : ℝ)
def economics_gap_fill_beats_sota_headlines : ℕ := 2
def economics_gap_fill_D_eff : ℕ := 20

theorem economics_gap_fill_observable_count_pos : 0 < economics_gap_fill_observable_count := by
  unfold economics_gap_fill_observable_count; decide

theorem economics_gap_fill_pooled_median_under_half_pct :
    economics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold economics_gap_fill_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem economics_gap_fill_headline_median_under_half_pct :
    economics_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold economics_gap_fill_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem economics_gap_fill_beats_sota_headlines_pos : 0 < economics_gap_fill_beats_sota_headlines := by
  unfold economics_gap_fill_beats_sota_headlines; decide

theorem economics_gap_fill_bundle :
    economics_gap_fill_observable_count = 157 ∧
    economics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    economics_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < economics_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold economics_gap_fill_observable_count; decide,
    economics_gap_fill_pooled_median_under_half_pct,
    economics_gap_fill_headline_median_under_half_pct,
    economics_gap_fill_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
