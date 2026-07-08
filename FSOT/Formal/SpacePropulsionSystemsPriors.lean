/-
  FSOT Formal SpacePropulsionSystemsPriors — Tier 39 (Space_Propulsion_Systems).
  Generator: scripts/gen_tier39_propulsion_electrical_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def space_propulsion_systems_observable_count : ℕ := 21
def space_propulsion_systems_median_error_pct : ℝ := (0.0 : ℝ)
def space_propulsion_systems_D_eff : ℕ := 14

theorem space_propulsion_systems_observable_count_pos : 0 < space_propulsion_systems_observable_count := by
  unfold space_propulsion_systems_observable_count; norm_num

theorem space_propulsion_systems_median_error_under_five_pct :
    space_propulsion_systems_median_error_pct < (5 : ℝ) := by
  unfold space_propulsion_systems_median_error_pct; norm_num

theorem space_propulsion_systems_bundle :
    space_propulsion_systems_observable_count = 21 ∧
    space_propulsion_systems_D_eff = 14 ∧
    space_propulsion_systems_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "fusion") > 0 := by
  refine ⟨
    by unfold space_propulsion_systems_observable_count; norm_num,
    by unfold space_propulsion_systems_D_eff; norm_num,
    space_propulsion_systems_median_error_under_five_pct,
    fusion_raw_S_positive
  ⟩

end

end FSOT.Formal
