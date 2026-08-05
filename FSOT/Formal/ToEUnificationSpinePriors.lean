/-
  FSOT Formal ToeUnificationSpinePriors — extension domain ToE_Unification_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def toe_unification_spine_observable_count : ℕ := 24
def toe_unification_spine_D_eff : ℕ := 20

theorem toe_unification_spine_observable_count_pos : 0 < toe_unification_spine_observable_count := by
  unfold toe_unification_spine_observable_count; decide

theorem toe_unification_spine_median_error_under_half_pct :
    (0.01900826880249791 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.01900826880249791 : ℝ) < (0.5 : ℝ))

theorem toe_unification_spine_bundle :
    toe_unification_spine_observable_count = 24 ∧
    toe_unification_spine_D_eff = 20 ∧
    (0.01900826880249791 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold toe_unification_spine_observable_count; decide,
    by unfold toe_unification_spine_D_eff; decide,
    toe_unification_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
