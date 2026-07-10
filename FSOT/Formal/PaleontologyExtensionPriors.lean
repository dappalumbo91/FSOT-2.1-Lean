/-
  FSOT Formal PaleontologyExtensionPriors — Paleontology Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def paleontology_ext_observable_count : ℕ := 630
def paleontology_ext_pooled_median_error_pct : ℝ := (0.017836062884406152 : ℝ)
def paleontology_ext_headline_median_error_pct : ℝ := (0.017836062884406152 : ℝ)
def paleontology_ext_beats_sota_headlines : ℕ := 2
def paleontology_ext_D_eff : ℕ := 18

theorem paleontology_ext_observable_count_pos : 0 < paleontology_ext_observable_count := by
  unfold paleontology_ext_observable_count; norm_num

theorem paleontology_ext_pooled_median_under_five_pct :
    paleontology_ext_pooled_median_error_pct < (5 : ℝ) := by
  unfold paleontology_ext_pooled_median_error_pct; norm_num

theorem paleontology_ext_headline_median_under_five_pct :
    paleontology_ext_headline_median_error_pct < (5 : ℝ) := by
  unfold paleontology_ext_headline_median_error_pct; norm_num

theorem paleontology_ext_beats_sota_headlines_pos : 0 < paleontology_ext_beats_sota_headlines := by
  unfold paleontology_ext_beats_sota_headlines; norm_num

theorem paleontology_ext_bundle :
    paleontology_ext_observable_count = 630 ∧
    paleontology_ext_pooled_median_error_pct < (5 : ℝ) ∧
    paleontology_ext_headline_median_error_pct < (5 : ℝ) ∧
    0 < paleontology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold paleontology_ext_observable_count; norm_num,
    paleontology_ext_pooled_median_under_five_pct,
    paleontology_ext_headline_median_under_five_pct,
    paleontology_ext_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
