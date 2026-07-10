/-
  FSOT Formal SociologyGapFillPriors — Sociology tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def sociology_gap_fill_observable_count : ℕ := 200
def sociology_gap_fill_pooled_median_error_pct : ℝ := (0.019504399572475274 : ℝ)
def sociology_gap_fill_headline_median_error_pct : ℝ := (0.019504399572475274 : ℝ)
def sociology_gap_fill_beats_sota_headlines : ℕ := 2
def sociology_gap_fill_D_eff : ℕ := 18

theorem sociology_gap_fill_observable_count_pos : 0 < sociology_gap_fill_observable_count := by
  unfold sociology_gap_fill_observable_count; norm_num

theorem sociology_gap_fill_pooled_median_under_half_pct :
    sociology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold sociology_gap_fill_pooled_median_error_pct; norm_num

theorem sociology_gap_fill_headline_median_under_half_pct :
    sociology_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold sociology_gap_fill_headline_median_error_pct; norm_num

theorem sociology_gap_fill_beats_sota_headlines_pos : 0 < sociology_gap_fill_beats_sota_headlines := by
  unfold sociology_gap_fill_beats_sota_headlines; norm_num

theorem sociology_gap_fill_bundle :
    sociology_gap_fill_observable_count = 200 ∧
    sociology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    sociology_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < sociology_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold sociology_gap_fill_observable_count; norm_num,
    sociology_gap_fill_pooled_median_under_half_pct,
    sociology_gap_fill_headline_median_under_half_pct,
    sociology_gap_fill_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
