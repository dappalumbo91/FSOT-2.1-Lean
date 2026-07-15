/-
  FSOT Formal ArxivPrimitivesPanelPriors — Tier 88 application wiring (Arxiv_Primitives_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def arxiv_primitives_observable_count : ℕ := 22
def arxiv_primitives_median_error_pct : ℝ := (0.031506 : ℝ)
def arxiv_primitives_D_eff : ℕ := 15

theorem arxiv_primitives_observable_count_pos : 0 < arxiv_primitives_observable_count := by
  unfold arxiv_primitives_observable_count; norm_num

theorem arxiv_primitives_median_error_under_five_pct :
    arxiv_primitives_median_error_pct < (5 : ℝ) := by
  unfold arxiv_primitives_median_error_pct; norm_num

theorem arxiv_primitives_bundle :
    arxiv_primitives_observable_count = 22 ∧
    arxiv_primitives_D_eff = 15 ∧
    arxiv_primitives_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold arxiv_primitives_observable_count; norm_num,
    by unfold arxiv_primitives_D_eff; norm_num,
    arxiv_primitives_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
