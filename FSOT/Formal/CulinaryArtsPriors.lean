/-
  FSOT Formal CulinaryArtsPriors — SMILES food chemistry + recipe process observables.
  Generator: scripts/gen_culinary_arts_lean.py
  Source: vendor/culinary_arts
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def culinary_arts_observable_count : ℕ := 26
def culinary_arts_section_count : ℕ := 8
def culinary_arts_D_eff : ℕ := 15
def culinary_arts_pooled_median_error_pct : ℝ := (0.047615187057821064 : ℝ)
def culinary_arts_headline_median_error_pct : ℝ := (0.047615187057821064 : ℝ)
def culinary_arts_beats_sota_headlines : ℕ := 7

theorem culinary_arts_observable_count_pos : 0 < culinary_arts_observable_count := by
  unfold culinary_arts_observable_count; norm_num

theorem culinary_arts_section_count_pos : 0 < culinary_arts_section_count := by
  unfold culinary_arts_section_count; norm_num

theorem culinary_arts_pooled_median_under_five_pct :
    culinary_arts_pooled_median_error_pct < (5 : ℝ) := by
  unfold culinary_arts_pooled_median_error_pct; norm_num

theorem culinary_arts_headline_median_under_five_pct :
    culinary_arts_headline_median_error_pct < (5 : ℝ) := by
  unfold culinary_arts_headline_median_error_pct; norm_num

theorem culinary_arts_beats_sota_headlines_pos : 0 < culinary_arts_beats_sota_headlines := by
  unfold culinary_arts_beats_sota_headlines; norm_num

theorem culinary_arts_bundle :
    culinary_arts_observable_count = 26 ∧
    culinary_arts_section_count = 8 ∧
    culinary_arts_D_eff = 15 ∧
    culinary_arts_pooled_median_error_pct < (5 : ℝ) ∧
    culinary_arts_headline_median_error_pct < (5 : ℝ) ∧
    0 < culinary_arts_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold culinary_arts_observable_count; norm_num,
    by unfold culinary_arts_section_count; norm_num,
    by unfold culinary_arts_D_eff; norm_num,
    culinary_arts_pooled_median_under_five_pct,
    culinary_arts_headline_median_under_five_pct,
    culinary_arts_beats_sota_headlines_pos,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
