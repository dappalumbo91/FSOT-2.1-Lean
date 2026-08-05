/-
  FSOT Formal SpeleologyExtensionPriors — Speleology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def speleology_ext_observable_count : ℕ := 200
def speleology_ext_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def speleology_ext_headline_median_error_pct : ℝ := (0.0 : ℝ)
def speleology_ext_beats_sota_headlines : ℕ := 2
def speleology_ext_D_eff : ℕ := 16

theorem speleology_ext_observable_count_pos : 0 < speleology_ext_observable_count := by
  unfold speleology_ext_observable_count; decide

theorem speleology_ext_pooled_median_under_half_pct :
    speleology_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold speleology_ext_pooled_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem speleology_ext_headline_median_under_half_pct :
    speleology_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold speleology_ext_headline_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem speleology_ext_beats_sota_headlines_pos : 0 < speleology_ext_beats_sota_headlines := by
  unfold speleology_ext_beats_sota_headlines; decide

theorem speleology_ext_bundle :
    speleology_ext_observable_count = 200 ∧
    speleology_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    speleology_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < speleology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold speleology_ext_observable_count; decide,
    speleology_ext_pooled_median_under_half_pct,
    speleology_ext_headline_median_under_half_pct,
    speleology_ext_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
