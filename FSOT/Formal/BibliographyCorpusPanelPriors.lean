/-
  FSOT Formal BibliographyCorpusPanelPriors — Tier 88 application wiring (Bibliography_Corpus_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def bibliography_corpus_observable_count : ℕ := 8
def bibliography_corpus_median_error_pct : ℝ := (0.013294 : ℝ)
def bibliography_corpus_D_eff : ℕ := 12

theorem bibliography_corpus_observable_count_pos : 0 < bibliography_corpus_observable_count := by
  unfold bibliography_corpus_observable_count; norm_num

theorem bibliography_corpus_median_error_under_five_pct :
    bibliography_corpus_median_error_pct < (5 : ℝ) := by
  unfold bibliography_corpus_median_error_pct; norm_num

theorem bibliography_corpus_bundle :
    bibliography_corpus_observable_count = 8 ∧
    bibliography_corpus_D_eff = 12 ∧
    bibliography_corpus_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "mathematical") > 0 := by
  refine ⟨
    by unfold bibliography_corpus_observable_count; norm_num,
    by unfold bibliography_corpus_D_eff; norm_num,
    bibliography_corpus_median_error_under_five_pct,
    mathematical_raw_S_positive
  ⟩

end

end FSOT.Formal
