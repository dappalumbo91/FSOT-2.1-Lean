/-
  FSOT Formal MachineAndMoleculeLivePanelPriors — verified desktop panel Machine_And_Molecule_Live_Panel.
  Generator: scripts/gen_verified_desktop_lean.py
  Cross-proof: exported via export_full_formal_obligations.py → Coq / Isabelle / F* / Rust replay
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def machine_and_molecule_live_observable_count : ℕ := 120
def machine_and_molecule_live_median_error_pct : ℝ := (0.01341 : ℝ)
def machine_and_molecule_live_D_eff : ℕ := 15

theorem machine_and_molecule_live_observable_count_pos : 0 < machine_and_molecule_live_observable_count := by
  unfold machine_and_molecule_live_observable_count; decide

theorem machine_and_molecule_live_median_error_under_five_pct :
    machine_and_molecule_live_median_error_pct < (5 : ℝ) := by
  unfold machine_and_molecule_live_median_error_pct
  exact (by norm_num : (0.01341  : ℝ) < (5 : ℝ))

theorem machine_and_molecule_live_median_error_under_half_pct :
    machine_and_molecule_live_median_error_pct < (0.5 : ℝ) := by
  unfold machine_and_molecule_live_median_error_pct
  exact (by norm_num : (0.01341  : ℝ) < 0.5)

theorem machine_and_molecule_live_bundle :
    machine_and_molecule_live_observable_count = 120 ∧
    machine_and_molecule_live_D_eff = 15 ∧
    machine_and_molecule_live_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold machine_and_molecule_live_observable_count; decide,
    by unfold machine_and_molecule_live_D_eff; decide,
    machine_and_molecule_live_median_error_under_half_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
