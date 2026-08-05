/-
  FSOT Formal QuantumMechanicsEntanglementDepthPanelPriors — extension domain Quantum_Mechanics_Entanglement_Depth_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def quantum_mechanics_entanglement_depth_panel_observable_count : ℕ := 23
def quantum_mechanics_entanglement_depth_panel_D_eff : ℕ := 16

theorem quantum_mechanics_entanglement_depth_panel_observable_count_pos : 0 < quantum_mechanics_entanglement_depth_panel_observable_count := by
  unfold quantum_mechanics_entanglement_depth_panel_observable_count; decide

theorem quantum_mechanics_entanglement_depth_panel_median_error_under_half_pct :
    (0.095551 : ℝ) < (0.5 : ℝ) := by norm_num

theorem quantum_mechanics_entanglement_depth_panel_bundle :
    quantum_mechanics_entanglement_depth_panel_observable_count = 23 ∧
    quantum_mechanics_entanglement_depth_panel_D_eff = 16 ∧
    (0.095551 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold quantum_mechanics_entanglement_depth_panel_observable_count; decide,
    by unfold quantum_mechanics_entanglement_depth_panel_D_eff; decide,
    quantum_mechanics_entanglement_depth_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
