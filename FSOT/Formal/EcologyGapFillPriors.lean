/-
  FSOT Formal EcologyGapFillPriors — Ecology tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def ecology_gap_fill_observable_count : ℕ := 627
def ecology_gap_fill_pooled_median_error_pct : ℝ := (0.017789000308164337 : ℝ)
def ecology_gap_fill_headline_median_error_pct : ℝ := (0.017789000308164337 : ℝ)
def ecology_gap_fill_beats_sota_headlines : ℕ := 3
def ecology_gap_fill_D_eff : ℕ := 14

theorem ecology_gap_fill_observable_count_pos : 0 < ecology_gap_fill_observable_count := by
  unfold ecology_gap_fill_observable_count; norm_num

theorem ecology_gap_fill_pooled_median_under_half_pct :
    ecology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold ecology_gap_fill_pooled_median_error_pct; norm_num

theorem ecology_gap_fill_headline_median_under_half_pct :
    ecology_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold ecology_gap_fill_headline_median_error_pct; norm_num

theorem ecology_gap_fill_beats_sota_headlines_pos : 0 < ecology_gap_fill_beats_sota_headlines := by
  unfold ecology_gap_fill_beats_sota_headlines; norm_num

theorem ecology_gap_fill_bundle :
    ecology_gap_fill_observable_count = 627 ∧
    ecology_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    ecology_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < ecology_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold ecology_gap_fill_observable_count; norm_num,
    ecology_gap_fill_pooled_median_under_half_pct,
    ecology_gap_fill_headline_median_under_half_pct,
    ecology_gap_fill_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
