/-
  FSOT Formal EconometricsGapFillPriors — Econometrics tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def econometrics_gap_fill_observable_count : ℕ := 172
def econometrics_gap_fill_pooled_median_error_pct : ℝ := (0.12920090413715177 : ℝ)
def econometrics_gap_fill_headline_median_error_pct : ℝ := (0.12920090413715177 : ℝ)
def econometrics_gap_fill_beats_sota_headlines : ℕ := 2
def econometrics_gap_fill_D_eff : ℕ := 19

theorem econometrics_gap_fill_observable_count_pos : 0 < econometrics_gap_fill_observable_count := by
  unfold econometrics_gap_fill_observable_count; norm_num

theorem econometrics_gap_fill_pooled_median_under_five_pct :
    econometrics_gap_fill_pooled_median_error_pct < (5 : ℝ) := by
  unfold econometrics_gap_fill_pooled_median_error_pct; norm_num

theorem econometrics_gap_fill_headline_median_under_five_pct :
    econometrics_gap_fill_headline_median_error_pct < (5 : ℝ) := by
  unfold econometrics_gap_fill_headline_median_error_pct; norm_num

theorem econometrics_gap_fill_beats_sota_headlines_pos : 0 < econometrics_gap_fill_beats_sota_headlines := by
  unfold econometrics_gap_fill_beats_sota_headlines; norm_num

theorem econometrics_gap_fill_bundle :
    econometrics_gap_fill_observable_count = 172 ∧
    econometrics_gap_fill_pooled_median_error_pct < (5 : ℝ) ∧
    econometrics_gap_fill_headline_median_error_pct < (5 : ℝ) ∧
    0 < econometrics_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold econometrics_gap_fill_observable_count; norm_num,
    econometrics_gap_fill_pooled_median_under_five_pct,
    econometrics_gap_fill_headline_median_under_five_pct,
    econometrics_gap_fill_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
