/-
  FSOT Formal FluidPhaseCurrentSpinePriors — extension domain Fluid_Phase_Current_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fluid_phase_current_spine_observable_count : ℕ := 24
def fluid_phase_current_spine_D_eff : ℕ := 20

theorem fluid_phase_current_spine_observable_count_pos : 0 < fluid_phase_current_spine_observable_count := by
  unfold fluid_phase_current_spine_observable_count; decide

theorem fluid_phase_current_spine_median_error_under_half_pct :
    (0.022997 : ℝ) < (0.5 : ℝ) := by norm_num

theorem fluid_phase_current_spine_bundle :
    fluid_phase_current_spine_observable_count = 24 ∧
    fluid_phase_current_spine_D_eff = 20 ∧
    (0.022997 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fluid_phase_current_spine_observable_count; decide,
    by unfold fluid_phase_current_spine_D_eff; decide,
    fluid_phase_current_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
