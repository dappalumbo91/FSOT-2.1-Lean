/-
  FSOT Formal ArxivBrainKnowledgePanelPriors — Tier 88 application wiring (Arxiv_Brain_Knowledge_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def arxiv_brain_observable_count : ℕ := 20
def arxiv_brain_median_error_pct : ℝ := (0.018003 : ℝ)
def arxiv_brain_D_eff : ℕ := 16

theorem arxiv_brain_observable_count_pos : 0 < arxiv_brain_observable_count := by
  unfold arxiv_brain_observable_count; norm_num

theorem arxiv_brain_median_error_under_five_pct :
    arxiv_brain_median_error_pct < (5 : ℝ) := by
  unfold arxiv_brain_median_error_pct; norm_num

theorem arxiv_brain_bundle :
    arxiv_brain_observable_count = 20 ∧
    arxiv_brain_D_eff = 16 ∧
    arxiv_brain_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "neural") > 0 := by
  refine ⟨
    by unfold arxiv_brain_observable_count; norm_num,
    by unfold arxiv_brain_D_eff; norm_num,
    arxiv_brain_median_error_under_five_pct,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
