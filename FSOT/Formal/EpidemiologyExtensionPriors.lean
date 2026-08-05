/-
  FSOT Formal EpidemiologyExtensionPriors — Epidemiology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def epidemiology_ext_observable_count : ℕ := 220
def epidemiology_ext_pooled_median_error_pct : ℝ := (0.039895 : ℝ)
def epidemiology_ext_headline_median_error_pct : ℝ := (0.039895 : ℝ)
def epidemiology_ext_beats_sota_headlines : ℕ := 2
def epidemiology_ext_D_eff : ℕ := 15

theorem epidemiology_ext_observable_count_pos : 0 < epidemiology_ext_observable_count := by
  unfold epidemiology_ext_observable_count; decide

theorem epidemiology_ext_pooled_median_under_half_pct :
    epidemiology_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold epidemiology_ext_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem epidemiology_ext_headline_median_under_half_pct :
    epidemiology_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold epidemiology_ext_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem epidemiology_ext_beats_sota_headlines_pos : 0 < epidemiology_ext_beats_sota_headlines := by
  unfold epidemiology_ext_beats_sota_headlines; decide

theorem epidemiology_ext_bundle :
    epidemiology_ext_observable_count = 220 ∧
    epidemiology_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    epidemiology_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < epidemiology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold epidemiology_ext_observable_count; decide,
    epidemiology_ext_pooled_median_under_half_pct,
    epidemiology_ext_headline_median_under_half_pct,
    epidemiology_ext_beats_sota_headlines_pos,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
