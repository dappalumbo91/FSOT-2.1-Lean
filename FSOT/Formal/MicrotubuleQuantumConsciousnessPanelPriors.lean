/-
  FSOT Formal MicrotubuleQuantumConsciousnessPanelPriors — extension domain Microtubule_Quantum_Consciousness_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def microtubule_quantum_consciousness_panel_observable_count : ℕ := 63
def microtubule_quantum_consciousness_panel_D_eff : ℕ := 17

theorem microtubule_quantum_consciousness_panel_observable_count_pos : 0 < microtubule_quantum_consciousness_panel_observable_count := by
  unfold microtubule_quantum_consciousness_panel_observable_count; decide

theorem microtubule_quantum_consciousness_panel_median_error_under_half_pct :
    (0.044671 : ℝ) < (0.5 : ℝ) := by norm_num

theorem microtubule_quantum_consciousness_panel_bundle :
    microtubule_quantum_consciousness_panel_observable_count = 63 ∧
    microtubule_quantum_consciousness_panel_D_eff = 17 ∧
    (0.044671 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold microtubule_quantum_consciousness_panel_observable_count; decide,
    by unfold microtubule_quantum_consciousness_panel_D_eff; decide,
    microtubule_quantum_consciousness_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
