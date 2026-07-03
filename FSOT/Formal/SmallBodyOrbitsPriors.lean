/-
  FSOT Formal SmallBodyOrbitsPriors — Moon/asteroid/comet JPL orbit checks.
  Generator: scripts/gen_small_body_orbits_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def small_body_orbit_count : ℕ := 5
def small_body_median_error_pct : ℝ := (0.014433 : ℝ)
def small_body_D_eff : ℕ := 18

theorem small_body_orbit_count_pos : 0 < small_body_orbit_count := by
  unfold small_body_orbit_count; norm_num

theorem small_body_median_error_under_eight_pct :
    small_body_median_error_pct < (8 : ℝ) := by
  unfold small_body_median_error_pct; norm_num

theorem small_body_orbits_bundle :
    small_body_orbit_count = 5 ∧
    small_body_D_eff = 18 ∧
    small_body_median_error_pct < (8 : ℝ) ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold small_body_orbit_count; norm_num,
    by unfold small_body_D_eff; norm_num,
    small_body_median_error_under_eight_pct,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
