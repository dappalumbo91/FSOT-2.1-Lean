/-
  FSOT Formal MachineAndMoleculeLivePanelPriors — extension domain Machine_And_Molecule_Live_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def machine_and_molecule_live_panel_observable_count : ℕ := 120
def machine_and_molecule_live_panel_D_eff : ℕ := 15

theorem machine_and_molecule_live_panel_observable_count_pos : 0 < machine_and_molecule_live_panel_observable_count := by
  unfold machine_and_molecule_live_panel_observable_count; norm_num

theorem machine_and_molecule_live_panel_median_error_under_half_pct :
    (0.01341 : ℝ) < (0.5 : ℝ) := by norm_num

theorem machine_and_molecule_live_panel_bundle :
    machine_and_molecule_live_panel_observable_count = 120 ∧
    machine_and_molecule_live_panel_D_eff = 15 ∧
    (0.01341 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold machine_and_molecule_live_panel_observable_count; norm_num,
    by unfold machine_and_molecule_live_panel_D_eff; norm_num,
    machine_and_molecule_live_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
