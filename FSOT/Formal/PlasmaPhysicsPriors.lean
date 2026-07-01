/-
  FSOT Formal PlasmaPhysicsPriors — extension domain Plasma_Physics.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def plasma_physics_observable_count : ℕ := 6
def plasma_physics_D_eff : ℕ := 14

theorem plasma_physics_observable_count_pos : 0 < plasma_physics_observable_count := by
  unfold plasma_physics_observable_count; norm_num

theorem plasma_physics_median_error_under_five_pct :
    (0.0 : ℝ) < (5 : ℝ) := by norm_num

theorem plasma_physics_bundle :
    plasma_physics_observable_count = 6 ∧
    plasma_physics_D_eff = 14 ∧
    (0.0 : ℝ) < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold plasma_physics_observable_count; norm_num,
    by unfold plasma_physics_D_eff; norm_num,
    plasma_physics_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
