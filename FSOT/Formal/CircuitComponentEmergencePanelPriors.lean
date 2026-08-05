/-
  FSOT Formal CircuitComponentEmergencePanelPriors — Tier 96 circuit emergence (Circuit_Component_Emergence_Panel).
  Generator: scripts/gen_circuit_component_emergence_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def circuit_component_emergence_observable_count : ℕ := 23
def circuit_component_emergence_median_error_pct : ℝ := (0.051887 : ℝ)
def circuit_component_emergence_D_eff : ℕ := 10

theorem circuit_component_emergence_observable_count_pos : 0 < circuit_component_emergence_observable_count := by
  unfold circuit_component_emergence_observable_count; decide

theorem circuit_component_emergence_median_error_under_five_pct :
    circuit_component_emergence_median_error_pct < (5 : ℝ) := by
  unfold circuit_component_emergence_median_error_pct; norm_num

theorem circuit_component_emergence_bundle :
    circuit_component_emergence_observable_count = 23 ∧
    circuit_component_emergence_D_eff = 10 ∧
    circuit_component_emergence_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold circuit_component_emergence_observable_count; decide,
    by unfold circuit_component_emergence_D_eff; decide,
    circuit_component_emergence_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
