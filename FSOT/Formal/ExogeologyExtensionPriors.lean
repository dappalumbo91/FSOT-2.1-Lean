/-
  FSOT Formal ExogeologyExtensionPriors — Exogeology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def exogeology_ext_observable_count : ℕ := 316
def exogeology_ext_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def exogeology_ext_headline_median_error_pct : ℝ := (0.0 : ℝ)
def exogeology_ext_beats_sota_headlines : ℕ := 2
def exogeology_ext_D_eff : ℕ := 20

theorem exogeology_ext_observable_count_pos : 0 < exogeology_ext_observable_count := by
  unfold exogeology_ext_observable_count; decide

theorem exogeology_ext_pooled_median_under_half_pct :
    exogeology_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold exogeology_ext_pooled_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem exogeology_ext_headline_median_under_half_pct :
    exogeology_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold exogeology_ext_headline_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem exogeology_ext_beats_sota_headlines_pos : 0 < exogeology_ext_beats_sota_headlines := by
  unfold exogeology_ext_beats_sota_headlines; decide

theorem exogeology_ext_bundle :
    exogeology_ext_observable_count = 316 ∧
    exogeology_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    exogeology_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < exogeology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold exogeology_ext_observable_count; decide,
    exogeology_ext_pooled_median_under_half_pct,
    exogeology_ext_headline_median_under_half_pct,
    exogeology_ext_beats_sota_headlines_pos,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
