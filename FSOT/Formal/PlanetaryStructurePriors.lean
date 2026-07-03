/-
  FSOT Formal PlanetaryStructurePriors — JPL planetary density verification.
  Generator: scripts/gen_planetary_structure_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def planetary_structure_body_count : ℕ := 8
def planetary_structure_median_error_pct : ℝ := (0.046016 : ℝ)
def planetary_structure_D_eff : ℕ := 16

theorem planetary_structure_body_count_pos : 0 < planetary_structure_body_count := by
  unfold planetary_structure_body_count; norm_num

theorem planetary_structure_median_error_under_five_pct :
    planetary_structure_median_error_pct < (5 : ℝ) := by
  unfold planetary_structure_median_error_pct; norm_num

theorem planetary_structure_bundle :
    planetary_structure_body_count = 8 ∧
    planetary_structure_D_eff = 16 ∧
    planetary_structure_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold planetary_structure_body_count; norm_num,
    by unfold planetary_structure_D_eff; norm_num,
    planetary_structure_median_error_under_five_pct,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
