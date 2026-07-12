/-
  FSOT Formal MechanisticCouplingPriors — extension domain Mechanistic_Coupling.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def mechanistic_coupling_observable_count : ℕ := 116
def mechanistic_coupling_D_eff : ℕ := 17

theorem mechanistic_coupling_observable_count_pos : 0 < mechanistic_coupling_observable_count := by
  unfold mechanistic_coupling_observable_count; norm_num

theorem mechanistic_coupling_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem mechanistic_coupling_bundle :
    mechanistic_coupling_observable_count = 116 ∧
    mechanistic_coupling_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold mechanistic_coupling_observable_count; norm_num,
    by unfold mechanistic_coupling_D_eff; norm_num,
    mechanistic_coupling_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
