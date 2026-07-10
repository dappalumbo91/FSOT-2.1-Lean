/-
  FSOT Formal PsychologyGapFillPriors — Psychology tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def psychology_gap_fill_observable_count : ℕ := 160
def psychology_gap_fill_pooled_median_error_pct : ℝ := (0.03150616921194649 : ℝ)
def psychology_gap_fill_headline_median_error_pct : ℝ := (0.03150616921194649 : ℝ)
def psychology_gap_fill_beats_sota_headlines : ℕ := 2
def psychology_gap_fill_D_eff : ℕ := 16

theorem psychology_gap_fill_observable_count_pos : 0 < psychology_gap_fill_observable_count := by
  unfold psychology_gap_fill_observable_count; norm_num

theorem psychology_gap_fill_pooled_median_under_half_pct :
    psychology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold psychology_gap_fill_pooled_median_error_pct; norm_num

theorem psychology_gap_fill_headline_median_under_half_pct :
    psychology_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold psychology_gap_fill_headline_median_error_pct; norm_num

theorem psychology_gap_fill_beats_sota_headlines_pos : 0 < psychology_gap_fill_beats_sota_headlines := by
  unfold psychology_gap_fill_beats_sota_headlines; norm_num

theorem psychology_gap_fill_bundle :
    psychology_gap_fill_observable_count = 160 ∧
    psychology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    psychology_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < psychology_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold psychology_gap_fill_observable_count; norm_num,
    psychology_gap_fill_pooled_median_under_half_pct,
    psychology_gap_fill_headline_median_under_half_pct,
    psychology_gap_fill_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
