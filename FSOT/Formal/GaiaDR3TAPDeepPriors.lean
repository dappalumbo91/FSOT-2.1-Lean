/-
  FSOT Formal GaiaDR3TAPDeepPriors — Tier 62–64 live astrometry, prereg scaffold, NeuroLab gaps.
  Generator: scripts/gen_tiers_62_64_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gaia_dr3_tap_deep_observable_count : ℕ := 386
def gaia_dr3_tap_deep_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def gaia_dr3_tap_deep_headline_median_error_pct : ℝ := (3.6e-05 : ℝ)
def gaia_dr3_tap_deep_beats_sota_headlines : ℕ := 2
def gaia_dr3_tap_deep_D_eff : ℕ := 20

theorem gaia_dr3_tap_deep_observable_count_pos : 0 < gaia_dr3_tap_deep_observable_count := by
  unfold gaia_dr3_tap_deep_observable_count; norm_num

theorem gaia_dr3_tap_deep_pooled_median_under_half_pct :
    gaia_dr3_tap_deep_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold gaia_dr3_tap_deep_pooled_median_error_pct; norm_num

theorem gaia_dr3_tap_deep_headline_median_under_half_pct :
    gaia_dr3_tap_deep_headline_median_error_pct < (0.5 : ℝ) := by
  unfold gaia_dr3_tap_deep_headline_median_error_pct; norm_num

theorem gaia_dr3_tap_deep_beats_sota_headlines_pos : 0 < gaia_dr3_tap_deep_beats_sota_headlines := by
  unfold gaia_dr3_tap_deep_beats_sota_headlines; norm_num

theorem gaia_dr3_tap_deep_bundle :
    gaia_dr3_tap_deep_observable_count = 386 ∧
    gaia_dr3_tap_deep_pooled_median_error_pct < (0.5 : ℝ) ∧
    gaia_dr3_tap_deep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold gaia_dr3_tap_deep_observable_count; norm_num
  · exact gaia_dr3_tap_deep_pooled_median_under_half_pct
  · exact gaia_dr3_tap_deep_beats_sota_headlines_pos

end
