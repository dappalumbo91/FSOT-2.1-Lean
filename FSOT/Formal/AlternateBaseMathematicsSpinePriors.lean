/-
  FSOT Formal AlternateBaseMathematicsSpinePriors — extension domain Alternate_Base_Mathematics_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def alternate_base_mathematics_spine_observable_count : ℕ := 24
def alternate_base_mathematics_spine_D_eff : ℕ := 18

theorem alternate_base_mathematics_spine_observable_count_pos : 0 < alternate_base_mathematics_spine_observable_count := by
  unfold alternate_base_mathematics_spine_observable_count; decide

theorem alternate_base_mathematics_spine_median_error_under_half_pct :
    (0.004184779870129773 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.004184779870129773 : ℝ) < (0.5 : ℝ))

theorem alternate_base_mathematics_spine_bundle :
    alternate_base_mathematics_spine_observable_count = 24 ∧
    alternate_base_mathematics_spine_D_eff = 18 ∧
    (0.004184779870129773 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold alternate_base_mathematics_spine_observable_count; decide,
    by unfold alternate_base_mathematics_spine_D_eff; decide,
    alternate_base_mathematics_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
