/-
  FSOT Formal NeutrinoPhysicsPriors — Tier 82 scientific expansion (Neutrino_Physics_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neutrino_physics_observable_count : ℕ := 20
def neutrino_physics_median_error_pct : ℝ := (0.009504 : ℝ)
def neutrino_physics_D_eff : ℕ := 7

theorem neutrino_physics_observable_count_pos : 0 < neutrino_physics_observable_count := by
  unfold neutrino_physics_observable_count; norm_num

theorem neutrino_physics_median_error_under_five_pct :
    neutrino_physics_median_error_pct < (5 : ℝ) := by
  unfold neutrino_physics_median_error_pct; norm_num

theorem neutrino_physics_bundle :
    neutrino_physics_observable_count = 20 ∧
    neutrino_physics_D_eff = 7 ∧
    neutrino_physics_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold neutrino_physics_observable_count; norm_num,
    by unfold neutrino_physics_D_eff; norm_num,
    neutrino_physics_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
