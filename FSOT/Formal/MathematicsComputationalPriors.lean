/-
  FSOT Formal MathematicsComputationalPriors — math-generator FSOT comparisons.
  Generator: scripts/gen_mathematics_computational_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def mathematics_computational_observable_count : ℕ := 20
def mathematics_computational_median_error_pct : ℝ := (1.4090183367935627e-14 : ℝ)
def mathematics_computational_D_eff : ℕ := 17

theorem mathematics_computational_observable_count_pos : 0 < mathematics_computational_observable_count := by
  unfold mathematics_computational_observable_count; decide

theorem mathematics_computational_median_error_under_five_pct :
    mathematics_computational_median_error_pct < (5 : ℝ) := by
  unfold mathematics_computational_median_error_pct
  exact (by norm_num : (1.4090183367935627e-14  : ℝ) < (5 : ℝ))

theorem mathematics_computational_bundle :
    mathematics_computational_observable_count = 20 ∧
    mathematics_computational_D_eff = 17 ∧
    mathematics_computational_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold mathematics_computational_observable_count; decide,
    by unfold mathematics_computational_D_eff; decide,
    mathematics_computational_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
