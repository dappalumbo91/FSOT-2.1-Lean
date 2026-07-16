/-
  FSOT Formal SchematicNetlistIntrinsicPanelPriors — Tier 96 circuit emergence (Schematic_Netlist_Intrinsic_Panel).
  Generator: scripts/gen_circuit_component_emergence_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def schematic_netlist_intrinsic_observable_count : ℕ := 5
def schematic_netlist_intrinsic_median_error_pct : ℝ := (0.051887 : ℝ)
def schematic_netlist_intrinsic_D_eff : ℕ := 10

theorem schematic_netlist_intrinsic_observable_count_pos : 0 < schematic_netlist_intrinsic_observable_count := by
  unfold schematic_netlist_intrinsic_observable_count; norm_num

theorem schematic_netlist_intrinsic_median_error_under_five_pct :
    schematic_netlist_intrinsic_median_error_pct < (5 : ℝ) := by
  unfold schematic_netlist_intrinsic_median_error_pct; norm_num

theorem schematic_netlist_intrinsic_bundle :
    schematic_netlist_intrinsic_observable_count = 5 ∧
    schematic_netlist_intrinsic_D_eff = 10 ∧
    schematic_netlist_intrinsic_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold schematic_netlist_intrinsic_observable_count; norm_num,
    by unfold schematic_netlist_intrinsic_D_eff; norm_num,
    schematic_netlist_intrinsic_median_error_under_five_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
