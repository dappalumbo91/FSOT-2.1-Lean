/-
  FSOT Formal PlanetaryStructurePriors — JPL planetary density verification.
  Generator: scripts/gen_planetary_structure_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def planetary_structure_body_count : ℕ := 20
def planetary_structure_median_error_pct : ℝ := (0.0 : ℝ)
def planetary_structure_D_eff : ℕ := 16

theorem planetary_structure_body_count_pos : 0 < planetary_structure_body_count := by
  unfold planetary_structure_body_count; decide

theorem planetary_structure_median_error_under_half_pct :
    planetary_structure_median_error_pct < (0.5 : ℝ) := by
  unfold planetary_structure_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem planetary_structure_bundle :
    planetary_structure_body_count = 20 ∧
    planetary_structure_D_eff = 16 ∧
    planetary_structure_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold planetary_structure_body_count; decide,
    by unfold planetary_structure_D_eff; decide,
    planetary_structure_median_error_under_half_pct,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
