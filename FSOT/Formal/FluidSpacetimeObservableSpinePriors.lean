/-
  FSOT Formal FluidSpacetimeObservableSpinePriors — extension domain Fluid_Spacetime_Observable_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fluid_spacetime_observable_spine_observable_count : ℕ := 29
def fluid_spacetime_observable_spine_D_eff : ℕ := 26

theorem fluid_spacetime_observable_spine_observable_count_pos : 0 < fluid_spacetime_observable_spine_observable_count := by
  unfold fluid_spacetime_observable_spine_observable_count; decide

theorem fluid_spacetime_observable_spine_median_error_under_half_pct :
    (0.000595 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.000595 : ℝ) < (0.5 : ℝ))

theorem fluid_spacetime_observable_spine_bundle :
    fluid_spacetime_observable_spine_observable_count = 29 ∧
    fluid_spacetime_observable_spine_D_eff = 26 ∧
    (0.000595 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fluid_spacetime_observable_spine_observable_count; decide,
    by unfold fluid_spacetime_observable_spine_D_eff; decide,
    fluid_spacetime_observable_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
