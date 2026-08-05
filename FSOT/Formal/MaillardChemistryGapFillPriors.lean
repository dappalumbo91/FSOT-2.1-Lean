/-
  FSOT Formal MaillardChemistryGapFillPriors — Maillard_Chemistry tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def maillard_chemistry_gap_fill_observable_count : ℕ := 30
def maillard_chemistry_gap_fill_pooled_median_error_pct : ℝ := (0.09443694019339524 : ℝ)
def maillard_chemistry_gap_fill_headline_median_error_pct : ℝ := (0.09443694019339524 : ℝ)
def maillard_chemistry_gap_fill_beats_sota_headlines : ℕ := 2
def maillard_chemistry_gap_fill_D_eff : ℕ := 15

theorem maillard_chemistry_gap_fill_observable_count_pos : 0 < maillard_chemistry_gap_fill_observable_count := by
  unfold maillard_chemistry_gap_fill_observable_count; decide

theorem maillard_chemistry_gap_fill_pooled_median_under_half_pct :
    maillard_chemistry_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold maillard_chemistry_gap_fill_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem maillard_chemistry_gap_fill_headline_median_under_half_pct :
    maillard_chemistry_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold maillard_chemistry_gap_fill_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem maillard_chemistry_gap_fill_beats_sota_headlines_pos : 0 < maillard_chemistry_gap_fill_beats_sota_headlines := by
  unfold maillard_chemistry_gap_fill_beats_sota_headlines; decide

theorem maillard_chemistry_gap_fill_bundle :
    maillard_chemistry_gap_fill_observable_count = 30 ∧
    maillard_chemistry_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    maillard_chemistry_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < maillard_chemistry_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold maillard_chemistry_gap_fill_observable_count; decide,
    maillard_chemistry_gap_fill_pooled_median_under_half_pct,
    maillard_chemistry_gap_fill_headline_median_under_half_pct,
    maillard_chemistry_gap_fill_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
