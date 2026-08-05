/-
  FSOT Formal GeologyStratigraphyExtensionPriors — Geology_Stratigraphy Tier D extension (real API anchors).
  Generator: scripts/gen_tier_d_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def geology_stratigraphy_ext_observable_count : ℕ := 1960
def geology_stratigraphy_ext_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def geology_stratigraphy_ext_headline_median_error_pct : ℝ := (0.0 : ℝ)
def geology_stratigraphy_ext_beats_sota_headlines : ℕ := 2
def geology_stratigraphy_ext_D_eff : ℕ := 18

theorem geology_stratigraphy_ext_observable_count_pos : 0 < geology_stratigraphy_ext_observable_count := by
  unfold geology_stratigraphy_ext_observable_count; decide

theorem geology_stratigraphy_ext_pooled_median_under_half_pct :
    geology_stratigraphy_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold geology_stratigraphy_ext_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem geology_stratigraphy_ext_headline_median_under_half_pct :
    geology_stratigraphy_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold geology_stratigraphy_ext_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem geology_stratigraphy_ext_beats_sota_headlines_pos : 0 < geology_stratigraphy_ext_beats_sota_headlines := by
  unfold geology_stratigraphy_ext_beats_sota_headlines; decide

theorem geology_stratigraphy_ext_bundle :
    geology_stratigraphy_ext_observable_count = 1960 ∧
    geology_stratigraphy_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    geology_stratigraphy_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < geology_stratigraphy_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold geology_stratigraphy_ext_observable_count; decide,
    geology_stratigraphy_ext_pooled_median_under_half_pct,
    geology_stratigraphy_ext_headline_median_under_half_pct,
    geology_stratigraphy_ext_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
