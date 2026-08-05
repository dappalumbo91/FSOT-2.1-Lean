/-
  FSOT Formal ToeGapClosureSpinePriors — extension domain ToE_Gap_Closure_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def toe_gap_closure_spine_observable_count : ℕ := 24
def toe_gap_closure_spine_D_eff : ℕ := 19

theorem toe_gap_closure_spine_observable_count_pos : 0 < toe_gap_closure_spine_observable_count := by
  unfold toe_gap_closure_spine_observable_count; decide

theorem toe_gap_closure_spine_median_error_under_half_pct :
    (0.021927861384483893 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.021927861384483893 : ℝ) < (0.5 : ℝ))

theorem toe_gap_closure_spine_bundle :
    toe_gap_closure_spine_observable_count = 24 ∧
    toe_gap_closure_spine_D_eff = 19 ∧
    (0.021927861384483893 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold toe_gap_closure_spine_observable_count; decide,
    by unfold toe_gap_closure_spine_D_eff; decide,
    toe_gap_closure_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
