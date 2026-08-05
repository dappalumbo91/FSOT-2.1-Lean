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
  unfold oceanography_gap_fill_observable_count; decide

theorem oceanography_gap_fill_pooled_median_under_half_pct :
    oceanography_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold oceanography_gap_fill_pooled_median_error_pct
  exact (by norm_num : (0.03017272606768673  : ℝ) < 0.5)

theorem oceanography_gap_fill_headline_median_under_half_pct :
    oceanography_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold oceanography_gap_fill_headline_median_error_pct
  exact (by norm_num : (0.030172726067689837  : ℝ) < 0.5)

theorem oceanography_gap_fill_beats_sota_headlines_pos : 0 < oceanography_gap_fill_beats_sota_headlines := by
  unfold oceanography_gap_fill_beats_sota_headlines; decide

theorem oceanography_gap_fill_bundle :
    oceanography_gap_fill_observable_count = 65 ∧
    oceanography_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    oceanography_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < oceanography_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold oceanography_gap_fill_observable_count; decide,
    oceanography_gap_fill_pooled_median_under_half_pct,
    oceanography_gap_fill_headline_median_under_half_pct,
    oceanography_gap_fill_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
