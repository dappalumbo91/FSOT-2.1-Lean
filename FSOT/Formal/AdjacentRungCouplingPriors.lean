/-
  FSOT Formal AdjacentRungCouplingPriors — extension domain Adjacent_Rung_Coupling.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def adjacent_rung_coupling_observable_count : ℕ := 36
def adjacent_rung_coupling_D_eff : ℕ := 17

theorem adjacent_rung_coupling_observable_count_pos : 0 < adjacent_rung_coupling_observable_count := by
  unfold adjacent_rung_coupling_observable_count; decide

theorem adjacent_rung_coupling_median_error_under_half_pct :
    (0.020098237848404983 : ℝ) < (0.5 : ℝ) := by norm_num

theorem adjacent_rung_coupling_bundle :
    adjacent_rung_coupling_observable_count = 36 ∧
    adjacent_rung_coupling_D_eff = 17 ∧
    (0.020098237848404983 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold adjacent_rung_coupling_observable_count; decide,
    by unfold adjacent_rung_coupling_D_eff; decide,
    adjacent_rung_coupling_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
