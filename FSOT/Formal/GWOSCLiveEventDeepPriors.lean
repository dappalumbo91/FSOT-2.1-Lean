/-
  FSOT Formal GWOSCLiveEventDeepPriors — Tier 57/58 public interdisciplinary / live catalog.
  Generator: scripts/gen_tiers_57_58_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gwosc_live_event_deep_observable_count : ℕ := 191
def gwosc_live_event_deep_pooled_median_error_pct : ℝ := (0.008488 : ℝ)
def gwosc_live_event_deep_headline_median_error_pct : ℝ := (0.008488 : ℝ)
def gwosc_live_event_deep_beats_sota_headlines : ℕ := 3
def gwosc_live_event_deep_D_eff : ℕ := 20

theorem gwosc_live_event_deep_observable_count_pos : 0 < gwosc_live_event_deep_observable_count := by
  unfold gwosc_live_event_deep_observable_count; norm_num

theorem gwosc_live_event_deep_pooled_median_under_half_pct :
    gwosc_live_event_deep_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold gwosc_live_event_deep_pooled_median_error_pct; norm_num

theorem gwosc_live_event_deep_headline_median_under_half_pct :
    gwosc_live_event_deep_headline_median_error_pct < (0.5 : ℝ) := by
  unfold gwosc_live_event_deep_headline_median_error_pct; norm_num

theorem gwosc_live_event_deep_beats_sota_headlines_pos : 0 < gwosc_live_event_deep_beats_sota_headlines := by
  unfold gwosc_live_event_deep_beats_sota_headlines; norm_num

theorem gwosc_live_event_deep_bundle :
    gwosc_live_event_deep_observable_count = 191 ∧
    gwosc_live_event_deep_pooled_median_error_pct < (0.5 : ℝ) ∧
    gwosc_live_event_deep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold gwosc_live_event_deep_observable_count; norm_num
  · exact gwosc_live_event_deep_pooled_median_under_half_pct
  · exact gwosc_live_event_deep_beats_sota_headlines_pos

end
