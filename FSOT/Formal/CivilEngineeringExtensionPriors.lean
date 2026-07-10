/-
  FSOT Formal CivilEngineeringExtensionPriors — Civil_Engineering Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def civil_engineering_ext_observable_count : ℕ := 181
def civil_engineering_ext_pooled_median_error_pct : ℝ := (0.033525988073647546 : ℝ)
def civil_engineering_ext_headline_median_error_pct : ℝ := (0.033525988073647546 : ℝ)
def civil_engineering_ext_beats_sota_headlines : ℕ := 2
def civil_engineering_ext_D_eff : ℕ := 16

theorem civil_engineering_ext_observable_count_pos : 0 < civil_engineering_ext_observable_count := by
  unfold civil_engineering_ext_observable_count; norm_num

theorem civil_engineering_ext_pooled_median_under_half_pct :
    civil_engineering_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold civil_engineering_ext_pooled_median_error_pct; norm_num

theorem civil_engineering_ext_headline_median_under_half_pct :
    civil_engineering_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold civil_engineering_ext_headline_median_error_pct; norm_num

theorem civil_engineering_ext_beats_sota_headlines_pos : 0 < civil_engineering_ext_beats_sota_headlines := by
  unfold civil_engineering_ext_beats_sota_headlines; norm_num

theorem civil_engineering_ext_bundle :
    civil_engineering_ext_observable_count = 181 ∧
    civil_engineering_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    civil_engineering_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < civil_engineering_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold civil_engineering_ext_observable_count; norm_num,
    civil_engineering_ext_pooled_median_under_half_pct,
    civil_engineering_ext_headline_median_under_half_pct,
    civil_engineering_ext_beats_sota_headlines_pos,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
