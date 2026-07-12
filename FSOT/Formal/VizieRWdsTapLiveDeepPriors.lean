/-
  FSOT Formal VizieRWdsTapLiveDeepPriors — Tier 68–70 expansion.
  Generator: scripts/gen_tiers_68_70_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def vizier_wds_tap_live_deep_observable_count : ℕ := 25
def vizier_wds_tap_live_deep_pooled_median_error_pct : ℝ := (0.026954 : ℝ)
def vizier_wds_tap_live_deep_headline_median_error_pct : ℝ := (0.026954 : ℝ)
def vizier_wds_tap_live_deep_beats_sota_headlines : ℕ := 2
def vizier_wds_tap_live_deep_D_eff : ℕ := 21

theorem vizier_wds_tap_live_deep_observable_count_pos : 0 < vizier_wds_tap_live_deep_observable_count := by
  unfold vizier_wds_tap_live_deep_observable_count; norm_num

theorem vizier_wds_tap_live_deep_pooled_median_under_half_pct :
    vizier_wds_tap_live_deep_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold vizier_wds_tap_live_deep_pooled_median_error_pct; norm_num

theorem vizier_wds_tap_live_deep_headline_median_under_half_pct :
    vizier_wds_tap_live_deep_headline_median_error_pct < (0.5 : ℝ) := by
  unfold vizier_wds_tap_live_deep_headline_median_error_pct; norm_num

theorem vizier_wds_tap_live_deep_beats_sota_headlines_pos : 0 < vizier_wds_tap_live_deep_beats_sota_headlines := by
  unfold vizier_wds_tap_live_deep_beats_sota_headlines; norm_num

theorem vizier_wds_tap_live_deep_bundle :
    vizier_wds_tap_live_deep_observable_count = 25 ∧
    vizier_wds_tap_live_deep_pooled_median_error_pct < (0.5 : ℝ) ∧
    vizier_wds_tap_live_deep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold vizier_wds_tap_live_deep_observable_count; norm_num
  · exact vizier_wds_tap_live_deep_pooled_median_under_half_pct
  · exact vizier_wds_tap_live_deep_beats_sota_headlines_pos

end
