/-
  FSOT Formal DarkSectorOpenProblemsPriors — Dark_Sector_Open_Problems Tier 51 stumped observables spine.
  Generator: scripts/gen_stumped_observables_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def dark_sector_observable_count : ℕ := 7
def dark_sector_pooled_median_error_pct : ℝ := (0.006335 : ℝ)
def dark_sector_headline_median_error_pct : ℝ := (0.006335 : ℝ)
def dark_sector_beats_sota_headlines : ℕ := 2
def dark_sector_D_eff : ℕ := 24

theorem dark_sector_observable_count_pos : 0 < dark_sector_observable_count := by
  unfold dark_sector_observable_count; norm_num

theorem dark_sector_pooled_median_under_half_pct :
    dark_sector_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold dark_sector_pooled_median_error_pct; norm_num

theorem dark_sector_headline_median_under_half_pct :
    dark_sector_headline_median_error_pct < (0.5 : ℝ) := by
  unfold dark_sector_headline_median_error_pct; norm_num

theorem dark_sector_beats_sota_headlines_pos : 0 < dark_sector_beats_sota_headlines := by
  unfold dark_sector_beats_sota_headlines; norm_num

theorem dark_sector_bundle :
    dark_sector_observable_count = 7 ∧
    dark_sector_pooled_median_error_pct < (0.5 : ℝ) ∧
    dark_sector_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold dark_sector_observable_count; norm_num
  · exact dark_sector_pooled_median_under_half_pct
  · exact dark_sector_beats_sota_headlines_pos

end
