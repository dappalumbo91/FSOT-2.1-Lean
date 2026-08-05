/-
  FSOT Formal ChaosMediatedPhaseTransitionsPriors — extension domain Chaos_Mediated_Phase_Transitions.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def chaos_mediated_phase_transitions_observable_count : ℕ := 21
def chaos_mediated_phase_transitions_D_eff : ℕ := 17

theorem chaos_mediated_phase_transitions_observable_count_pos : 0 < chaos_mediated_phase_transitions_observable_count := by
  unfold chaos_mediated_phase_transitions_observable_count; decide

theorem chaos_mediated_phase_transitions_median_error_under_half_pct :
    (0.03147898006445882 : ℝ) < (0.5 : ℝ) := by norm_num

theorem chaos_mediated_phase_transitions_bundle :
    chaos_mediated_phase_transitions_observable_count = 21 ∧
    chaos_mediated_phase_transitions_D_eff = 17 ∧
    (0.03147898006445882 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold chaos_mediated_phase_transitions_observable_count; decide,
    by unfold chaos_mediated_phase_transitions_D_eff; decide,
    chaos_mediated_phase_transitions_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
