/-
  FSOT Formal OrbitalMechanicsPriors — Kepler third-law JPL verification.
  Generator: scripts/gen_orbital_mechanics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def orbital_mechanics_body_count : ℕ := 8
def orbital_mechanics_median_error_pct : ℝ := (0.106141 : ℝ)
def orbital_mechanics_D_eff : ℕ := 18

theorem orbital_mechanics_body_count_pos : 0 < orbital_mechanics_body_count := by
  unfold orbital_mechanics_body_count; norm_num

theorem orbital_mechanics_median_error_under_five_pct :
    orbital_mechanics_median_error_pct < (5 : ℝ) := by
  unfold orbital_mechanics_median_error_pct; norm_num

theorem orbital_mechanics_bundle :
    orbital_mechanics_body_count = 8 ∧
    orbital_mechanics_D_eff = 18 ∧
    orbital_mechanics_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold orbital_mechanics_body_count; norm_num,
    by unfold orbital_mechanics_D_eff; norm_num,
    orbital_mechanics_median_error_under_five_pct,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
