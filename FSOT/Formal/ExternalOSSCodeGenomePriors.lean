/-
  FSOT Formal ExternalOSSCodeGenomePriors — External_OSS_Code_Genome Tier I programming verification.
  Generator: scripts/gen_tier_i_programming_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def external_oss_observable_count : ℕ := 169
def external_oss_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def external_oss_headline_median_error_pct : ℝ := (0.0 : ℝ)
def external_oss_beats_sota_headlines : ℕ := 2
def external_oss_D_eff : ℕ := 16

def external_oss_oss_sample_count : ℕ := 23
def external_oss_high_affinity_pair_count : ℕ := 34

theorem external_oss_observable_count_pos : 0 < external_oss_observable_count := by
  unfold external_oss_observable_count; norm_num

theorem external_oss_pooled_median_under_five_pct :
    external_oss_pooled_median_error_pct < (5 : ℝ) := by
  unfold external_oss_pooled_median_error_pct; norm_num

theorem external_oss_headline_median_under_five_pct :
    external_oss_headline_median_error_pct < (5 : ℝ) := by
  unfold external_oss_headline_median_error_pct; norm_num

theorem external_oss_beats_sota_headlines_pos : 0 < external_oss_beats_sota_headlines := by
  unfold external_oss_beats_sota_headlines; norm_num

theorem external_oss_oss_samples_pos : 0 < external_oss_oss_sample_count := by
  unfold external_oss_oss_sample_count; norm_num

theorem external_oss_bundle :
    external_oss_observable_count = 169 ∧
    external_oss_pooled_median_error_pct < (5 : ℝ) ∧
    external_oss_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold external_oss_observable_count; norm_num
  · exact external_oss_pooled_median_under_five_pct
  · exact external_oss_beats_sota_headlines_pos

end
