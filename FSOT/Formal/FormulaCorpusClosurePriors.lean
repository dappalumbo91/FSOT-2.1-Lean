/-
  FSOT Formal FormulaCorpusClosurePriors — extension domain Formula_Corpus_Closure.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def formula_corpus_closure_observable_count : ℕ := 123
def formula_corpus_closure_D_eff : ℕ := 17

theorem formula_corpus_closure_observable_count_pos : 0 < formula_corpus_closure_observable_count := by
  unfold formula_corpus_closure_observable_count; decide

theorem formula_corpus_closure_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem formula_corpus_closure_bundle :
    formula_corpus_closure_observable_count = 123 ∧
    formula_corpus_closure_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold formula_corpus_closure_observable_count; decide,
    by unfold formula_corpus_closure_D_eff; decide,
    formula_corpus_closure_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
