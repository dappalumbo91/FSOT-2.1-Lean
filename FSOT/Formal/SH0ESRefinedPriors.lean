/-
  FSOT Formal SH0ESRefinedPriors — SH0ES_Refined Tier 51 anomaly observables.
  Generator: scripts/gen_anomaly_observables_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def sh0es_refined_observable_count : ℕ := 7
def sh0es_refined_pooled_median_error_pct : ℝ := (0.462181 : ℝ)
def sh0es_refined_headline_median_error_pct : ℝ := (0.462181 : ℝ)
def sh0es_refined_beats_sota_headlines : ℕ := 2
def sh0es_refined_D_eff : ℕ := 25
def sh0es_refined_host_count : ℕ := 46

theorem sh0es_refined_observable_count_pos : 0 < sh0es_refined_observable_count := by
  unfold sh0es_refined_observable_count; norm_num

theorem sh0es_refined_pooled_median_under_half_pct :
    sh0es_refined_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold sh0es_refined_pooled_median_error_pct; norm_num

theorem sh0es_refined_headline_median_under_half_pct :
    sh0es_refined_headline_median_error_pct < (0.5 : ℝ) := by
  unfold sh0es_refined_headline_median_error_pct; norm_num

theorem sh0es_refined_beats_sota_headlines_pos : 0 < sh0es_refined_beats_sota_headlines := by
  unfold sh0es_refined_beats_sota_headlines; norm_num
theorem sh0es_refined_hosts_pos : 0 < sh0es_refined_host_count := by unfold sh0es_refined_host_count; norm_num

theorem sh0es_refined_bundle :
    sh0es_refined_observable_count = 7 ∧
    sh0es_refined_pooled_median_error_pct < (0.5 : ℝ) ∧
    sh0es_refined_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold sh0es_refined_observable_count; norm_num
  · exact sh0es_refined_pooled_median_under_half_pct
  · exact sh0es_refined_beats_sota_headlines_pos

end
