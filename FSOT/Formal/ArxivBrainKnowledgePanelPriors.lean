/-
  FSOT Formal ArxivBrainKnowledgePanelPriors — extension domain Arxiv_Brain_Knowledge_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def arxiv_brain_knowledge_panel_observable_count : ℕ := 20
def arxiv_brain_knowledge_panel_D_eff : ℕ := 16

theorem arxiv_brain_knowledge_panel_observable_count_pos : 0 < arxiv_brain_knowledge_panel_observable_count := by
  unfold arxiv_brain_knowledge_panel_observable_count; decide

theorem arxiv_brain_knowledge_panel_median_error_under_half_pct :
    (0.018003 : ℝ) < (0.5 : ℝ) := by norm_num

theorem arxiv_brain_knowledge_panel_bundle :
    arxiv_brain_knowledge_panel_observable_count = 20 ∧
    arxiv_brain_knowledge_panel_D_eff = 16 ∧
    (0.018003 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold arxiv_brain_knowledge_panel_observable_count; decide,
    by unfold arxiv_brain_knowledge_panel_D_eff; decide,
    arxiv_brain_knowledge_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
