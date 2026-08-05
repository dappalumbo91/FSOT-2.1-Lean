/-
  FSOT Formal PharmacokineticsGapFillPriors — Pharmacokinetics tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pharmacokinetics_gap_fill_observable_count : ℕ := 56
def pharmacokinetics_gap_fill_pooled_median_error_pct : ℝ := (0.00241237063663613 : ℝ)
def pharmacokinetics_gap_fill_headline_median_error_pct : ℝ := (0.04593318440797578 : ℝ)
def pharmacokinetics_gap_fill_beats_sota_headlines : ℕ := 2
def pharmacokinetics_gap_fill_D_eff : ℕ := 14

theorem pharmacokinetics_gap_fill_observable_count_pos : 0 < pharmacokinetics_gap_fill_observable_count := by
  unfold pharmacokinetics_gap_fill_observable_count; decide

theorem pharmacokinetics_gap_fill_pooled_median_under_half_pct :
    pharmacokinetics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold pharmacokinetics_gap_fill_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem pharmacokinetics_gap_fill_headline_median_under_half_pct :
    pharmacokinetics_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold pharmacokinetics_gap_fill_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem pharmacokinetics_gap_fill_beats_sota_headlines_pos : 0 < pharmacokinetics_gap_fill_beats_sota_headlines := by
  unfold pharmacokinetics_gap_fill_beats_sota_headlines; decide

theorem pharmacokinetics_gap_fill_bundle :
    pharmacokinetics_gap_fill_observable_count = 56 ∧
    pharmacokinetics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    pharmacokinetics_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < pharmacokinetics_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold pharmacokinetics_gap_fill_observable_count; decide,
    pharmacokinetics_gap_fill_pooled_median_under_half_pct,
    pharmacokinetics_gap_fill_headline_median_under_half_pct,
    pharmacokinetics_gap_fill_beats_sota_headlines_pos,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
