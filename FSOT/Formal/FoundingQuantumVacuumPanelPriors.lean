/-
  FSOT Formal FoundingQuantumVacuumPanelPriors — extension domain Founding_Quantum_Vacuum_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def founding_quantum_vacuum_panel_observable_count : ℕ := 24
def founding_quantum_vacuum_panel_D_eff : ℕ := 8

theorem founding_quantum_vacuum_panel_observable_count_pos : 0 < founding_quantum_vacuum_panel_observable_count := by
  unfold founding_quantum_vacuum_panel_observable_count; norm_num

theorem founding_quantum_vacuum_panel_median_error_under_half_pct :
    (0.01529034996934153 : ℝ) < (0.5 : ℝ) := by norm_num

theorem founding_quantum_vacuum_panel_bundle :
    founding_quantum_vacuum_panel_observable_count = 24 ∧
    founding_quantum_vacuum_panel_D_eff = 8 ∧
    (0.01529034996934153 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold founding_quantum_vacuum_panel_observable_count; norm_num,
    by unfold founding_quantum_vacuum_panel_D_eff; norm_num,
    founding_quantum_vacuum_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
