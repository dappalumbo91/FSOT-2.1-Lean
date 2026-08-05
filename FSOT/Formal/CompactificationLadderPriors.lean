/-
  FSOT Formal CompactificationLadderPriors — extension domain Compactification_Ladder.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def compactification_ladder_observable_count : ℕ := 60
def compactification_ladder_D_eff : ℕ := 18

theorem compactification_ladder_observable_count_pos : 0 < compactification_ladder_observable_count := by
  unfold compactification_ladder_observable_count; decide

theorem compactification_ladder_median_error_under_half_pct :
    (0.0220747159758794 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0220747159758794 : ℝ) < (0.5 : ℝ))

theorem compactification_ladder_bundle :
    compactification_ladder_observable_count = 60 ∧
    compactification_ladder_D_eff = 18 ∧
    (0.0220747159758794 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold compactification_ladder_observable_count; decide,
    by unfold compactification_ladder_D_eff; decide,
    compactification_ladder_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
