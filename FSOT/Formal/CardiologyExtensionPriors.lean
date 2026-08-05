/-
  FSOT Formal CardiologyExtensionPriors — Cardiology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def cardiology_ext_observable_count : ℕ := 126
def cardiology_ext_pooled_median_error_pct : ℝ := (0.030622122938654326 : ℝ)
def cardiology_ext_headline_median_error_pct : ℝ := (0.030622122938654326 : ℝ)
def cardiology_ext_beats_sota_headlines : ℕ := 2
def cardiology_ext_D_eff : ℕ := 15

theorem cardiology_ext_observable_count_pos : 0 < cardiology_ext_observable_count := by
  unfold cardiology_ext_observable_count; decide

theorem cardiology_ext_pooled_median_under_half_pct :
    cardiology_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold cardiology_ext_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem cardiology_ext_headline_median_under_half_pct :
    cardiology_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold cardiology_ext_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem cardiology_ext_beats_sota_headlines_pos : 0 < cardiology_ext_beats_sota_headlines := by
  unfold cardiology_ext_beats_sota_headlines; decide

theorem cardiology_ext_bundle :
    cardiology_ext_observable_count = 126 ∧
    cardiology_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    cardiology_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < cardiology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold cardiology_ext_observable_count; decide,
    cardiology_ext_pooled_median_under_half_pct,
    cardiology_ext_headline_median_under_half_pct,
    cardiology_ext_beats_sota_headlines_pos,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
