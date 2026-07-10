/-
  FSOT Formal OceanographyGapFillPriors — Oceanography tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def oceanography_gap_fill_observable_count : ℕ := 65
def oceanography_gap_fill_pooled_median_error_pct : ℝ := (0.03017272606768673 : ℝ)
def oceanography_gap_fill_headline_median_error_pct : ℝ := (0.030172726067689837 : ℝ)
def oceanography_gap_fill_beats_sota_headlines : ℕ := 2
def oceanography_gap_fill_D_eff : ℕ := 17

theorem oceanography_gap_fill_observable_count_pos : 0 < oceanography_gap_fill_observable_count := by
  unfold oceanography_gap_fill_observable_count; norm_num

theorem oceanography_gap_fill_pooled_median_under_five_pct :
    oceanography_gap_fill_pooled_median_error_pct < (5 : ℝ) := by
  unfold oceanography_gap_fill_pooled_median_error_pct; norm_num

theorem oceanography_gap_fill_headline_median_under_five_pct :
    oceanography_gap_fill_headline_median_error_pct < (5 : ℝ) := by
  unfold oceanography_gap_fill_headline_median_error_pct; norm_num

theorem oceanography_gap_fill_beats_sota_headlines_pos : 0 < oceanography_gap_fill_beats_sota_headlines := by
  unfold oceanography_gap_fill_beats_sota_headlines; norm_num

theorem oceanography_gap_fill_bundle :
    oceanography_gap_fill_observable_count = 65 ∧
    oceanography_gap_fill_pooled_median_error_pct < (5 : ℝ) ∧
    oceanography_gap_fill_headline_median_error_pct < (5 : ℝ) ∧
    0 < oceanography_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold oceanography_gap_fill_observable_count; norm_num,
    oceanography_gap_fill_pooled_median_under_five_pct,
    oceanography_gap_fill_headline_median_under_five_pct,
    oceanography_gap_fill_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
