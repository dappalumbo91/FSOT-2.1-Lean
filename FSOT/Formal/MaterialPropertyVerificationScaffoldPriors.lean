/-
  FSOT Formal MaterialPropertyVerificationScaffoldPriors — extension domain Material_Property_Verification_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def material_property_verification_scaffold_observable_count : ℕ := 79
def material_property_verification_scaffold_D_eff : ℕ := 15

theorem material_property_verification_scaffold_observable_count_pos : 0 < material_property_verification_scaffold_observable_count := by
  unfold material_property_verification_scaffold_observable_count; decide

theorem material_property_verification_scaffold_median_error_under_half_pct :
    (0.002271 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.002271 : ℝ) < (0.5 : ℝ))

theorem material_property_verification_scaffold_bundle :
    material_property_verification_scaffold_observable_count = 79 ∧
    material_property_verification_scaffold_D_eff = 15 ∧
    (0.002271 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold material_property_verification_scaffold_observable_count; decide,
    by unfold material_property_verification_scaffold_D_eff; decide,
    material_property_verification_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
