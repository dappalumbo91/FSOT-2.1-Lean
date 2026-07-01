/-
  FSOT Formal ThesisSimulationPriors — Tier 15 thesis simulation lab observables.
  Source: data/thesis_simulation_benchmark.json (wave7–10 + intrinsic screens)
  Generator: scripts/gen_thesis_simulation_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def thesis_wave_target_count : ℕ := 98
def thesis_intrinsic_screen_count : ℕ := 58
def thesis_simulation_observable_count : ℕ := 156
def thesis_wave_file_count : ℕ := 4
def thesis_intrinsic_best_rmse : ℝ := (6.763968608085996 : ℝ)

theorem thesis_wave_target_count_pos : 0 < thesis_wave_target_count := by
  unfold thesis_wave_target_count; norm_num

theorem thesis_intrinsic_screen_count_pos : 0 < thesis_intrinsic_screen_count := by
  unfold thesis_intrinsic_screen_count; norm_num

theorem thesis_simulation_observable_count_pos : 0 < thesis_simulation_observable_count := by
  unfold thesis_simulation_observable_count; norm_num

theorem thesis_intrinsic_best_rmse_positive : (0 : ℝ) < thesis_intrinsic_best_rmse := by
  unfold thesis_intrinsic_best_rmse; norm_num

theorem thesis_simulation_components_le_total :
    thesis_wave_target_count + thesis_intrinsic_screen_count = thesis_simulation_observable_count := by
  unfold thesis_wave_target_count thesis_intrinsic_screen_count thesis_simulation_observable_count; norm_num

/-- Bundle: wave observations + intrinsic formula screens with particle-domain sign proxy. -/
theorem thesis_simulation_bundle :
    thesis_wave_target_count = 98 ∧
    thesis_intrinsic_screen_count = 58 ∧
    thesis_simulation_observable_count = 156 ∧
    thesis_wave_file_count = 4 ∧
    thesis_wave_target_count + thesis_intrinsic_screen_count = thesis_simulation_observable_count ∧
    (0 : ℝ) < raw_S (get_domain_params "particle") := by
  refine ⟨
    by unfold thesis_wave_target_count; norm_num,
    by unfold thesis_intrinsic_screen_count; norm_num,
    by unfold thesis_simulation_observable_count; norm_num,
    by unfold thesis_wave_file_count; norm_num,
    thesis_simulation_components_le_total,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
