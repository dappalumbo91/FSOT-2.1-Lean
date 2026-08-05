/-
  FSOT Formal FormulaCorpusCncPriors — Formula corpus + CNC controller bundle.
  Generator: scripts/gen_formula_corpus_cnc_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def formula_corpus_cnc_observable_count : ℕ := 10
def formula_corpus_cnc_median_error_pct : ℝ := (0.0 : ℝ)
def formula_corpus_cnc_D_eff : ℕ := 17

theorem formula_corpus_cnc_observable_count_pos : 0 < formula_corpus_cnc_observable_count := by
  unfold formula_corpus_cnc_observable_count; decide

theorem formula_corpus_cnc_median_error_under_five_pct :
    formula_corpus_cnc_median_error_pct < (5 : ℝ) := by
  unfold formula_corpus_cnc_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem formula_corpus_cnc_bundle :
    formula_corpus_cnc_observable_count = 10 ∧
    formula_corpus_cnc_D_eff = 17 ∧
    formula_corpus_cnc_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold formula_corpus_cnc_observable_count; decide,
    by unfold formula_corpus_cnc_D_eff; decide,
    formula_corpus_cnc_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
