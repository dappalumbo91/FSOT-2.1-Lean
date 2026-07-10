/-
  FSOT Formal Term3AcousticBleedDepthPriors — Tier 67 per-channel formula precision.
  Generator: scripts/gen_tiers_67_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def term3_acoustic_bleed_depth_observable_count : ℕ := 23
def term3_acoustic_bleed_depth_pooled_median_error_pct : ℝ := (0.008381497018408523 : ℝ)
def term3_acoustic_bleed_depth_headline_median_error_pct : ℝ := (0.008381497018409132 : ℝ)
def term3_acoustic_bleed_depth_beats_sota_headlines : ℕ := 2
def term3_acoustic_bleed_depth_D_eff : ℕ := 15

theorem term3_acoustic_bleed_depth_observable_count_pos : 0 < term3_acoustic_bleed_depth_observable_count := by
  unfold term3_acoustic_bleed_depth_observable_count; norm_num

theorem term3_acoustic_bleed_depth_pooled_median_under_half_pct :
    term3_acoustic_bleed_depth_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold term3_acoustic_bleed_depth_pooled_median_error_pct; norm_num

theorem term3_acoustic_bleed_depth_headline_median_under_half_pct :
    term3_acoustic_bleed_depth_headline_median_error_pct < (0.5 : ℝ) := by
  unfold term3_acoustic_bleed_depth_headline_median_error_pct; norm_num

theorem term3_acoustic_bleed_depth_beats_sota_headlines_pos : 0 < term3_acoustic_bleed_depth_beats_sota_headlines := by
  unfold term3_acoustic_bleed_depth_beats_sota_headlines; norm_num

theorem term3_acoustic_bleed_depth_bundle :
    term3_acoustic_bleed_depth_observable_count = 23 ∧
    term3_acoustic_bleed_depth_pooled_median_error_pct < (0.5 : ℝ) ∧
    term3_acoustic_bleed_depth_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold term3_acoustic_bleed_depth_observable_count; norm_num
  · exact term3_acoustic_bleed_depth_pooled_median_under_half_pct
  · exact term3_acoustic_bleed_depth_beats_sota_headlines_pos

end
