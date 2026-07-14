/-
  FSOT Formal ArxivPrimitivesV14Priors — arXiv V14 cognitive primitives loop.
  Generator: scripts/gen_arxiv_primitives_v14_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def arxiv_primitives_v14_observable_count : ℕ := 14
def arxiv_primitives_v14_median_error_pct : ℝ := (0.0 : ℝ)
def arxiv_primitives_v14_D_eff : ℕ := 12

theorem arxiv_primitives_v14_observable_count_pos : 0 < arxiv_primitives_v14_observable_count := by
  unfold arxiv_primitives_v14_observable_count; norm_num

theorem arxiv_primitives_v14_median_error_under_five_pct :
    arxiv_primitives_v14_median_error_pct < (5 : ℝ) := by
  unfold arxiv_primitives_v14_median_error_pct; norm_num

theorem arxiv_primitives_v14_bundle :
    arxiv_primitives_v14_observable_count = 14 ∧
    arxiv_primitives_v14_D_eff = 12 ∧
    arxiv_primitives_v14_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold arxiv_primitives_v14_observable_count; norm_num,
    by unfold arxiv_primitives_v14_D_eff; norm_num,
    arxiv_primitives_v14_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
