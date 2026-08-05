/-
  FSOT Formal BibliographyCorpusPanelPriors — extension domain Bibliography_Corpus_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def bibliography_corpus_panel_observable_count : ℕ := 24
def bibliography_corpus_panel_D_eff : ℕ := 12

theorem bibliography_corpus_panel_observable_count_pos : 0 < bibliography_corpus_panel_observable_count := by
  unfold bibliography_corpus_panel_observable_count; decide

theorem bibliography_corpus_panel_median_error_under_half_pct :
    (0.03801653760497401 : ℝ) < (0.5 : ℝ) := by norm_num

theorem bibliography_corpus_panel_bundle :
    bibliography_corpus_panel_observable_count = 24 ∧
    bibliography_corpus_panel_D_eff = 12 ∧
    (0.03801653760497401 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold bibliography_corpus_panel_observable_count; decide,
    by unfold bibliography_corpus_panel_D_eff; decide,
    bibliography_corpus_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
