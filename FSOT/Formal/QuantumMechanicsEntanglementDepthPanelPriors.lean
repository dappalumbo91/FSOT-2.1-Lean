/-
  FSOT Formal QuantumMechanicsEntanglementDepthPanelPriors — Tier 87 depth wave (Quantum_Mechanics_Entanglement_Depth_Panel).
  Generator: scripts/gen_tier87_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_mechanics_entanglement_depth_observable_count : ℕ := 11
def quantum_mechanics_entanglement_depth_median_error_pct : ℝ := (0.095551 : ℝ)
def quantum_mechanics_entanglement_depth_D_eff : ℕ := 16

theorem quantum_mechanics_entanglement_depth_observable_count_pos : 0 < quantum_mechanics_entanglement_depth_observable_count := by
  unfold quantum_mechanics_entanglement_depth_observable_count; norm_num

theorem quantum_mechanics_entanglement_depth_median_error_under_five_pct :
    quantum_mechanics_entanglement_depth_median_error_pct < (5 : ℝ) := by
  unfold quantum_mechanics_entanglement_depth_median_error_pct; norm_num

theorem quantum_mechanics_entanglement_depth_bundle :
    quantum_mechanics_entanglement_depth_observable_count = 11 ∧
    quantum_mechanics_entanglement_depth_D_eff = 16 ∧
    quantum_mechanics_entanglement_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "quantum") > 0 := by
  refine ⟨
    by unfold quantum_mechanics_entanglement_depth_observable_count; norm_num,
    by unfold quantum_mechanics_entanglement_depth_D_eff; norm_num,
    quantum_mechanics_entanglement_depth_median_error_under_five_pct,
    quantum_raw_S_positive
  ⟩

end

end FSOT.Formal
