/-
  FSOT Formal ZoologyExtensionPriors — Zoology Tier D extension (real API anchors).
  Generator: scripts/gen_tier_d_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def zoology_ext_observable_count : ℕ := 1000
def zoology_ext_pooled_median_error_pct : ℝ := (0.01778900030815634 : ℝ)
def zoology_ext_headline_median_error_pct : ℝ := (0.01778900030815634 : ℝ)
def zoology_ext_beats_sota_headlines : ℕ := 2
def zoology_ext_D_eff : ℕ := 14

theorem zoology_ext_observable_count_pos : 0 < zoology_ext_observable_count := by
  unfold zoology_ext_observable_count; decide

theorem zoology_ext_pooled_median_under_half_pct :
    zoology_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold zoology_ext_pooled_median_error_pct
  exact (by norm_num : (0.01778900030815634  : ℝ) < 0.5)

theorem zoology_ext_headline_median_under_half_pct :
    zoology_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold zoology_ext_headline_median_error_pct
  exact (by norm_num : (0.01778900030815634  : ℝ) < 0.5)

theorem zoology_ext_beats_sota_headlines_pos : 0 < zoology_ext_beats_sota_headlines := by
  unfold zoology_ext_beats_sota_headlines; decide

theorem zoology_ext_bundle :
    zoology_ext_observable_count = 1000 ∧
    zoology_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    zoology_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < zoology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold zoology_ext_observable_count; decide,
    zoology_ext_pooled_median_under_half_pct,
    zoology_ext_headline_median_under_half_pct,
    zoology_ext_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
