/-
  FSOT Formal ChemicalEngineeringExtensionPriors — Chemical_Engineering Tier D extension (real API anchors).
  Generator: scripts/gen_tier_d_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def chemical_engineering_ext_observable_count : ℕ := 186
def chemical_engineering_ext_pooled_median_error_pct : ℝ := (0.0010333425185953097 : ℝ)
def chemical_engineering_ext_headline_median_error_pct : ℝ := (0.0010333425185953097 : ℝ)
def chemical_engineering_ext_beats_sota_headlines : ℕ := 2
def chemical_engineering_ext_D_eff : ℕ := 16

theorem chemical_engineering_ext_observable_count_pos : 0 < chemical_engineering_ext_observable_count := by
  unfold chemical_engineering_ext_observable_count; norm_num

theorem chemical_engineering_ext_pooled_median_under_half_pct :
    chemical_engineering_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold chemical_engineering_ext_pooled_median_error_pct; norm_num

theorem chemical_engineering_ext_headline_median_under_half_pct :
    chemical_engineering_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold chemical_engineering_ext_headline_median_error_pct; norm_num

theorem chemical_engineering_ext_beats_sota_headlines_pos : 0 < chemical_engineering_ext_beats_sota_headlines := by
  unfold chemical_engineering_ext_beats_sota_headlines; norm_num

theorem chemical_engineering_ext_bundle :
    chemical_engineering_ext_observable_count = 186 ∧
    chemical_engineering_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    chemical_engineering_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < chemical_engineering_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "chemical") > 0 := by
  refine ⟨
    by unfold chemical_engineering_ext_observable_count; norm_num,
    chemical_engineering_ext_pooled_median_under_half_pct,
    chemical_engineering_ext_headline_median_under_half_pct,
    chemical_engineering_ext_beats_sota_headlines_pos,
    chemical_raw_S_positive
  ⟩

end

end FSOT.Formal
