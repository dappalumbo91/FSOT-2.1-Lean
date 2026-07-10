/-
  FSOT Formal MycologyExtensionPriors — Mycology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def mycology_ext_observable_count : ℕ := 420
def mycology_ext_pooled_median_error_pct : ℝ := (0.022236250385193498 : ℝ)
def mycology_ext_headline_median_error_pct : ℝ := (0.022236250385193498 : ℝ)
def mycology_ext_beats_sota_headlines : ℕ := 2
def mycology_ext_D_eff : ℕ := 14

theorem mycology_ext_observable_count_pos : 0 < mycology_ext_observable_count := by
  unfold mycology_ext_observable_count; norm_num

theorem mycology_ext_pooled_median_under_five_pct :
    mycology_ext_pooled_median_error_pct < (5 : ℝ) := by
  unfold mycology_ext_pooled_median_error_pct; norm_num

theorem mycology_ext_headline_median_under_five_pct :
    mycology_ext_headline_median_error_pct < (5 : ℝ) := by
  unfold mycology_ext_headline_median_error_pct; norm_num

theorem mycology_ext_beats_sota_headlines_pos : 0 < mycology_ext_beats_sota_headlines := by
  unfold mycology_ext_beats_sota_headlines; norm_num

theorem mycology_ext_bundle :
    mycology_ext_observable_count = 420 ∧
    mycology_ext_pooled_median_error_pct < (5 : ℝ) ∧
    mycology_ext_headline_median_error_pct < (5 : ℝ) ∧
    0 < mycology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold mycology_ext_observable_count; norm_num,
    mycology_ext_pooled_median_under_five_pct,
    mycology_ext_headline_median_under_five_pct,
    mycology_ext_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
