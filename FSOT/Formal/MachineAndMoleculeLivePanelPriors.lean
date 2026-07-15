/-
  FSOT Formal MachineAndMoleculeLivePanelPriors — Tier 88 application wiring (Machine_And_Molecule_Live_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def machine_and_molecule_live_observable_count : ℕ := 120
def machine_and_molecule_live_median_error_pct : ℝ := (0.01341 : ℝ)
def machine_and_molecule_live_D_eff : ℕ := 15

theorem machine_and_molecule_live_observable_count_pos : 0 < machine_and_molecule_live_observable_count := by
  unfold machine_and_molecule_live_observable_count; norm_num

theorem machine_and_molecule_live_median_error_under_five_pct :
    machine_and_molecule_live_median_error_pct < (5 : ℝ) := by
  unfold machine_and_molecule_live_median_error_pct; norm_num

theorem machine_and_molecule_live_bundle :
    machine_and_molecule_live_observable_count = 120 ∧
    machine_and_molecule_live_D_eff = 15 ∧
    machine_and_molecule_live_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold machine_and_molecule_live_observable_count; norm_num,
    by unfold machine_and_molecule_live_D_eff; norm_num,
    machine_and_molecule_live_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
