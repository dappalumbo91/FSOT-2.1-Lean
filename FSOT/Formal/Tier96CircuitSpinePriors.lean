/-
  FSOT Formal Tier96CircuitSpinePriors — Tier 96 circuit emergence (Tier_96_Circuit_Spine).
  Generator: scripts/gen_circuit_component_emergence_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def tier_96_circuit_observable_count : ℕ := 11
def tier_96_circuit_median_error_pct : ℝ := (0.0 : ℝ)
def tier_96_circuit_D_eff : ℕ := 10

theorem tier_96_circuit_observable_count_pos : 0 < tier_96_circuit_observable_count := by
  unfold tier_96_circuit_observable_count; decide

theorem tier_96_circuit_median_error_under_five_pct :
    tier_96_circuit_median_error_pct < (5 : ℝ) := by
  unfold tier_96_circuit_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem tier_96_circuit_bundle :
    tier_96_circuit_observable_count = 11 ∧
    tier_96_circuit_D_eff = 10 ∧
    tier_96_circuit_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold tier_96_circuit_observable_count; decide,
    by unfold tier_96_circuit_D_eff; decide,
    tier_96_circuit_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
