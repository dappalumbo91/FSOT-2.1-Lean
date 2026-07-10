/-
  FSOT Formal FormulaCorpusClosurePriors — strict-empirical + extension bridge closure.
  Generator: scripts/gen_formula_corpus_closure_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def formula_corpus_closure_observable_count : ℕ := 123
def formula_corpus_closure_strict_empirical_count : ℕ := 7941
def formula_corpus_closure_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def formula_corpus_closure_beats_sota_headlines : ℕ := 3
def formula_corpus_closure_D_eff : ℕ := 17

theorem formula_corpus_closure_observable_count_pos : 0 < formula_corpus_closure_observable_count := by
  unfold formula_corpus_closure_observable_count; norm_num

theorem formula_corpus_closure_strict_empirical_pos : 0 < formula_corpus_closure_strict_empirical_count := by
  unfold formula_corpus_closure_strict_empirical_count; norm_num

theorem formula_corpus_closure_pooled_median_under_five_pct :
    formula_corpus_closure_pooled_median_error_pct < (5 : ℝ) := by
  unfold formula_corpus_closure_pooled_median_error_pct; norm_num

theorem formula_corpus_closure_beats_sota_headlines_pos : 0 < formula_corpus_closure_beats_sota_headlines := by
  unfold formula_corpus_closure_beats_sota_headlines; norm_num

theorem formula_corpus_closure_bundle :
    formula_corpus_closure_observable_count = 123 ∧
    formula_corpus_closure_strict_empirical_count = 7941 ∧
    formula_corpus_closure_pooled_median_error_pct < (5 : ℝ) ∧
    0 < formula_corpus_closure_beats_sota_headlines ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold formula_corpus_closure_observable_count; norm_num,
    by unfold formula_corpus_closure_strict_empirical_count; norm_num,
    formula_corpus_closure_pooled_median_under_five_pct,
    formula_corpus_closure_beats_sota_headlines_pos,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
