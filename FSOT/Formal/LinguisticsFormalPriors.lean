/-
  FSOT Formal LinguisticsFormalPriors — measured linguistic anchors.
  Generator: scripts/gen_linguistics_formal_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def linguistics_formal_observable_count : ℕ := 10
def linguistics_formal_median_error_pct : ℝ := (0.0013504254899468224 : ℝ)
def linguistics_formal_D_eff : ℕ := 12

theorem linguistics_formal_observable_count_pos : 0 < linguistics_formal_observable_count := by
  unfold linguistics_formal_observable_count; norm_num

theorem linguistics_formal_median_error_under_five_pct :
    linguistics_formal_median_error_pct < (5 : ℝ) := by
  unfold linguistics_formal_median_error_pct; norm_num

theorem linguistics_formal_bundle :
    linguistics_formal_observable_count = 10 ∧
    linguistics_formal_D_eff = 12 ∧
    linguistics_formal_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold linguistics_formal_observable_count; norm_num,
    by unfold linguistics_formal_D_eff; norm_num,
    linguistics_formal_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
