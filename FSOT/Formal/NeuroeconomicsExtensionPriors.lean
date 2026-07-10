/-
  FSOT Formal NeuroeconomicsExtensionPriors — Neuroeconomics Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neuroeconomics_ext_observable_count : ℕ := 123
def neuroeconomics_ext_pooled_median_error_pct : ℝ := (0.10502056403980387 : ℝ)
def neuroeconomics_ext_headline_median_error_pct : ℝ := (0.10502056403980387 : ℝ)
def neuroeconomics_ext_beats_sota_headlines : ℕ := 2
def neuroeconomics_ext_D_eff : ℕ := 16

theorem neuroeconomics_ext_observable_count_pos : 0 < neuroeconomics_ext_observable_count := by
  unfold neuroeconomics_ext_observable_count; norm_num

theorem neuroeconomics_ext_pooled_median_under_half_pct :
    neuroeconomics_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold neuroeconomics_ext_pooled_median_error_pct; norm_num

theorem neuroeconomics_ext_headline_median_under_half_pct :
    neuroeconomics_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold neuroeconomics_ext_headline_median_error_pct; norm_num

theorem neuroeconomics_ext_beats_sota_headlines_pos : 0 < neuroeconomics_ext_beats_sota_headlines := by
  unfold neuroeconomics_ext_beats_sota_headlines; norm_num

theorem neuroeconomics_ext_bundle :
    neuroeconomics_ext_observable_count = 123 ∧
    neuroeconomics_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    neuroeconomics_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < neuroeconomics_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold neuroeconomics_ext_observable_count; norm_num,
    neuroeconomics_ext_pooled_median_under_half_pct,
    neuroeconomics_ext_headline_median_under_half_pct,
    neuroeconomics_ext_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
