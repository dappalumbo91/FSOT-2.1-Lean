/-
  FSOT Formal VirologyExtensionPriors — Virology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def virology_ext_observable_count : ℕ := 163
def virology_ext_pooled_median_error_pct : ℝ := (0.04593318440798183 : ℝ)
def virology_ext_headline_median_error_pct : ℝ := (0.04593318440798183 : ℝ)
def virology_ext_beats_sota_headlines : ℕ := 2
def virology_ext_D_eff : ℕ := 14

theorem virology_ext_observable_count_pos : 0 < virology_ext_observable_count := by
  unfold virology_ext_observable_count; norm_num

theorem virology_ext_pooled_median_under_five_pct :
    virology_ext_pooled_median_error_pct < (5 : ℝ) := by
  unfold virology_ext_pooled_median_error_pct; norm_num

theorem virology_ext_headline_median_under_five_pct :
    virology_ext_headline_median_error_pct < (5 : ℝ) := by
  unfold virology_ext_headline_median_error_pct; norm_num

theorem virology_ext_beats_sota_headlines_pos : 0 < virology_ext_beats_sota_headlines := by
  unfold virology_ext_beats_sota_headlines; norm_num

theorem virology_ext_bundle :
    virology_ext_observable_count = 163 ∧
    virology_ext_pooled_median_error_pct < (5 : ℝ) ∧
    virology_ext_headline_median_error_pct < (5 : ℝ) ∧
    0 < virology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold virology_ext_observable_count; norm_num,
    virology_ext_pooled_median_under_five_pct,
    virology_ext_headline_median_under_five_pct,
    virology_ext_beats_sota_headlines_pos,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
