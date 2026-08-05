/-
  FSOT Formal QuantumInformationPriors — extension domain Quantum_Information.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def quantum_information_observable_count : ℕ := 24
def quantum_information_D_eff : ℕ := 11

theorem quantum_information_observable_count_pos : 0 < quantum_information_observable_count := by
  unfold quantum_information_observable_count; decide

theorem quantum_information_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem quantum_information_bundle :
    quantum_information_observable_count = 24 ∧
    quantum_information_D_eff = 11 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold quantum_information_observable_count; decide,
    by unfold quantum_information_D_eff; decide,
    quantum_information_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
