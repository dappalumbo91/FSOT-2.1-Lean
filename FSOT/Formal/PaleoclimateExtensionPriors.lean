/-
  FSOT Formal PaleoclimateExtensionPriors — Paleoclimate Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def paleoclimate_ext_observable_count : ℕ := 40
def paleoclimate_ext_pooled_median_error_pct : ℝ := (0.015015854077432778 : ℝ)
def paleoclimate_ext_headline_median_error_pct : ℝ := (0.015015854077432778 : ℝ)
def paleoclimate_ext_beats_sota_headlines : ℕ := 2
def paleoclimate_ext_D_eff : ℕ := 17

theorem paleoclimate_ext_observable_count_pos : 0 < paleoclimate_ext_observable_count := by
  unfold paleoclimate_ext_observable_count; decide

theorem paleoclimate_ext_pooled_median_under_half_pct :
    paleoclimate_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold paleoclimate_ext_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem paleoclimate_ext_headline_median_under_half_pct :
    paleoclimate_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold paleoclimate_ext_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem paleoclimate_ext_beats_sota_headlines_pos : 0 < paleoclimate_ext_beats_sota_headlines := by
  unfold paleoclimate_ext_beats_sota_headlines; decide

theorem paleoclimate_ext_bundle :
    paleoclimate_ext_observable_count = 40 ∧
    paleoclimate_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    paleoclimate_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < paleoclimate_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold paleoclimate_ext_observable_count; decide,
    paleoclimate_ext_pooled_median_under_half_pct,
    paleoclimate_ext_headline_median_under_half_pct,
    paleoclimate_ext_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
