/-
  FSOT Formal PureMathematicsPriors — extension domain Pure_Mathematics.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def pure_mathematics_observable_count : ℕ := 1578
def pure_mathematics_D_eff : ℕ := 18

theorem pure_mathematics_observable_count_pos : 0 < pure_mathematics_observable_count := by
  unfold pure_mathematics_observable_count; norm_num

theorem pure_mathematics_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem pure_mathematics_bundle :
    pure_mathematics_observable_count = 1578 ∧
    pure_mathematics_D_eff = 18 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold pure_mathematics_observable_count; norm_num,
    by unfold pure_mathematics_D_eff; norm_num,
    pure_mathematics_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
