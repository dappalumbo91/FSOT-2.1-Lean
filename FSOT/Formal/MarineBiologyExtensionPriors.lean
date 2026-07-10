/-
  FSOT Formal MarineBiologyExtensionPriors — Marine_Biology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def marine_biology_ext_observable_count : ℕ := 540
def marine_biology_ext_pooled_median_error_pct : ℝ := (0.022236250385192644 : ℝ)
def marine_biology_ext_headline_median_error_pct : ℝ := (0.022236250385194948 : ℝ)
def marine_biology_ext_beats_sota_headlines : ℕ := 2
def marine_biology_ext_D_eff : ℕ := 15

theorem marine_biology_ext_observable_count_pos : 0 < marine_biology_ext_observable_count := by
  unfold marine_biology_ext_observable_count; norm_num

theorem marine_biology_ext_pooled_median_under_five_pct :
    marine_biology_ext_pooled_median_error_pct < (5 : ℝ) := by
  unfold marine_biology_ext_pooled_median_error_pct; norm_num

theorem marine_biology_ext_headline_median_under_five_pct :
    marine_biology_ext_headline_median_error_pct < (5 : ℝ) := by
  unfold marine_biology_ext_headline_median_error_pct; norm_num

theorem marine_biology_ext_beats_sota_headlines_pos : 0 < marine_biology_ext_beats_sota_headlines := by
  unfold marine_biology_ext_beats_sota_headlines; norm_num

theorem marine_biology_ext_bundle :
    marine_biology_ext_observable_count = 540 ∧
    marine_biology_ext_pooled_median_error_pct < (5 : ℝ) ∧
    marine_biology_ext_headline_median_error_pct < (5 : ℝ) ∧
    0 < marine_biology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold marine_biology_ext_observable_count; norm_num,
    marine_biology_ext_pooled_median_under_five_pct,
    marine_biology_ext_headline_median_under_five_pct,
    marine_biology_ext_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
