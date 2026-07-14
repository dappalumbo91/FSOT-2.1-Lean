/-
  FSOT Formal TectonicsPriors — plate-boundary crustal earthquake coupling.
  Generator: scripts/gen_tectonics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def tectonics_event_count : ℕ := 500
def tectonics_boundary_count : ℕ := 241
def tectonics_match_count : ℕ := 500
def tectonics_D_eff : ℕ := 17
def tectonics_match_rate : ℝ := (1.0 : ℝ)

theorem tectonics_event_count_pos : 0 < tectonics_event_count := by
  unfold tectonics_event_count; norm_num

theorem tectonics_boundary_count_pos : 0 < tectonics_boundary_count := by
  unfold tectonics_boundary_count; norm_num

theorem tectonics_match_le_total : tectonics_match_count ≤ tectonics_event_count := by
  unfold tectonics_match_count tectonics_event_count; norm_num

theorem tectonics_bundle :
    tectonics_event_count = 500 ∧
    tectonics_boundary_count = 241 ∧
    tectonics_match_count = 500 ∧
    tectonics_D_eff = 17 ∧
    tectonics_match_count ≤ tectonics_event_count ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold tectonics_event_count; norm_num,
    by unfold tectonics_boundary_count; norm_num,
    by unfold tectonics_match_count; norm_num,
    by unfold tectonics_D_eff; norm_num,
    tectonics_match_le_total,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
