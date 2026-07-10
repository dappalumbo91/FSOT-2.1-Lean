/-
  FSOT Formal OncologyPriors — SMILES drug/enzyme + biology strict bridge.
  Generator: scripts/gen_oncology_lean.py
  Source: vendor/oncology
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def oncology_observable_count : ℕ := 67
def oncology_section_count : ℕ := 5
def oncology_D_eff : ℕ := 14
def oncology_pooled_median_error_pct : ℝ := (0.078779 : ℝ)
def oncology_headline_median_error_pct : ℝ := (0.078779 : ℝ)
def oncology_beats_sota_headlines : ℕ := 5

theorem oncology_observable_count_pos : 0 < oncology_observable_count := by
  unfold oncology_observable_count; norm_num

theorem oncology_section_count_pos : 0 < oncology_section_count := by
  unfold oncology_section_count; norm_num

theorem oncology_pooled_median_under_half_pct :
    oncology_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold oncology_pooled_median_error_pct; norm_num

theorem oncology_headline_median_under_half_pct :
    oncology_headline_median_error_pct < (0.5 : ℝ) := by
  unfold oncology_headline_median_error_pct; norm_num

theorem oncology_beats_sota_headlines_pos : 0 < oncology_beats_sota_headlines := by
  unfold oncology_beats_sota_headlines; norm_num

theorem oncology_bundle :
    oncology_observable_count = 67 ∧
    oncology_section_count = 5 ∧
    oncology_D_eff = 14 ∧
    oncology_pooled_median_error_pct < (0.5 : ℝ) ∧
    oncology_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < oncology_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold oncology_observable_count; norm_num,
    by unfold oncology_section_count; norm_num,
    by unfold oncology_D_eff; norm_num,
    oncology_pooled_median_under_half_pct,
    oncology_headline_median_under_half_pct,
    oncology_beats_sota_headlines_pos,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
