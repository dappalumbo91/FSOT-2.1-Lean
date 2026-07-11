/-
  FSOT Formal DarkSectorOpenProblemsPriors — Dark_Sector_Open_Problems Tier 51 stumped observables spine.
  Generator: scripts/gen_stumped_observables_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def dark_sector_observable_count : ℕ := 10
def dark_sector_pooled_median_error_pct : ℝ := (0.009407 : ℝ)
def dark_sector_headline_median_error_pct : ℝ := (0.009407 : ℝ)
def dark_sector_beats_sota_headlines : ℕ := 2
def dark_sector_D_eff : ℕ := 24
def dark_sector_w0_cmb : ℝ := (-1.0299812921372637 : ℝ)
def dark_sector_w0_bao : ℝ := (-0.7296790154668923 : ℝ)
def dark_sector_wa_cmb : ℝ := (-0.808109771581081 : ℝ)
def dark_sector_wa_bao : ℝ := (-1.0208556449829258 : ℝ)

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
theorem dark_sector_w0_cmb_negative : dark_sector_w0_cmb < (0 : ℝ) := by unfold dark_sector_w0_cmb; norm_num
theorem dark_sector_w0_bao_negative : dark_sector_w0_bao < (0 : ℝ) := by unfold dark_sector_w0_bao; norm_num
theorem dark_sector_wa_cmb_negative : dark_sector_wa_cmb < (0 : ℝ) := by unfold dark_sector_wa_cmb; norm_num
theorem dark_sector_wa_bao_negative : dark_sector_wa_bao < (0 : ℝ) := by unfold dark_sector_wa_bao; norm_num

theorem dark_sector_bundle :
    dark_sector_observable_count = 10 ∧
    dark_sector_pooled_median_error_pct < (0.5 : ℝ) ∧
    dark_sector_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold dark_sector_observable_count; norm_num
  · exact dark_sector_pooled_median_under_half_pct
  · exact dark_sector_beats_sota_headlines_pos

end
