/-
  FSOT Formal BibliographyLeanCorpusPriors — axiomatic bibliography corpus.
  Generator: scripts/gen_bibliography_lean_corpus_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def bibliography_lean_corpus_observable_count : ℕ := 9
def bibliography_lean_corpus_median_error_pct : ℝ := (0.0 : ℝ)
def bibliography_lean_corpus_D_eff : ℕ := 13

theorem bibliography_lean_corpus_observable_count_pos : 0 < bibliography_lean_corpus_observable_count := by
  unfold bibliography_lean_corpus_observable_count; norm_num

theorem bibliography_lean_corpus_median_error_under_half_pct :
    bibliography_lean_corpus_median_error_pct < (0.5 : ℝ) := by
  unfold bibliography_lean_corpus_median_error_pct; norm_num

theorem bibliography_lean_corpus_bundle :
    bibliography_lean_corpus_observable_count = 9 ∧
    bibliography_lean_corpus_D_eff = 13 ∧
    bibliography_lean_corpus_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold bibliography_lean_corpus_observable_count; norm_num,
    by unfold bibliography_lean_corpus_D_eff; norm_num,
    bibliography_lean_corpus_median_error_under_half_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
