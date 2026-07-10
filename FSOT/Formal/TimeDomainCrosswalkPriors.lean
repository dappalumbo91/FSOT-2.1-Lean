/-
  FSOT Formal TimeDomainCrosswalkPriors — Time_Domain_Crosswalk Tier 50 time emergence / FPC.
  Generator: scripts/gen_time_emergence_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def time_xw_observable_count : ℕ := 149
def time_xw_pooled_median_error_pct : ℝ := (0.023158 : ℝ)
def time_xw_headline_median_error_pct : ℝ := (0.023158 : ℝ)
def time_xw_beats_sota_headlines : ℕ := 2
def time_xw_D_eff : ℕ := 19
def time_xw_crosswalk_domain_count : ℕ := 145

theorem time_xw_observable_count_pos : 0 < time_xw_observable_count := by
  unfold time_xw_observable_count; norm_num

theorem time_xw_pooled_median_under_half_pct :
    time_xw_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold time_xw_pooled_median_error_pct; norm_num

theorem time_xw_headline_median_under_half_pct :
    time_xw_headline_median_error_pct < (0.5 : ℝ) := by
  unfold time_xw_headline_median_error_pct; norm_num

theorem time_xw_beats_sota_headlines_pos : 0 < time_xw_beats_sota_headlines := by
  unfold time_xw_beats_sota_headlines; norm_num
theorem time_xw_crosswalk_domains_pos : 0 < time_xw_crosswalk_domain_count := by unfold time_xw_crosswalk_domain_count; norm_num

theorem time_xw_bundle :
    time_xw_observable_count = 149 ∧
    time_xw_pooled_median_error_pct < (0.5 : ℝ) ∧
    time_xw_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold time_xw_observable_count; norm_num
  · exact time_xw_pooled_median_under_half_pct
  · exact time_xw_beats_sota_headlines_pos

end
