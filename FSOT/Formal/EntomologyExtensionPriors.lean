/-
  FSOT Formal EntomologyExtensionPriors — Entomology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def entomology_ext_observable_count : ℕ := 430
def entomology_ext_pooled_median_error_pct : ℝ := (0.022236250385189223 : ℝ)
def entomology_ext_headline_median_error_pct : ℝ := (0.022236250385189223 : ℝ)
def entomology_ext_beats_sota_headlines : ℕ := 2
def entomology_ext_D_eff : ℕ := 14

theorem entomology_ext_observable_count_pos : 0 < entomology_ext_observable_count := by
  unfold entomology_ext_observable_count; decide

theorem entomology_ext_pooled_median_under_half_pct :
    entomology_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold entomology_ext_pooled_median_error_pct
  exact (by norm_num : (0.022236250385189223  : ℝ) < 0.5)

theorem entomology_ext_headline_median_under_half_pct :
    entomology_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold entomology_ext_headline_median_error_pct
  exact (by norm_num : (0.022236250385189223  : ℝ) < 0.5)

theorem entomology_ext_beats_sota_headlines_pos : 0 < entomology_ext_beats_sota_headlines := by
  unfold entomology_ext_beats_sota_headlines; decide

theorem entomology_ext_bundle :
    entomology_ext_observable_count = 430 ∧
    entomology_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    entomology_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < entomology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold entomology_ext_observable_count; decide,
    entomology_ext_pooled_median_under_half_pct,
    entomology_ext_headline_median_under_half_pct,
    entomology_ext_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
