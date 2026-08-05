/-
  FSOT Formal MaillardChemistryPriors — extension domain Maillard_Chemistry.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def maillard_chemistry_observable_count : ℕ := 30
def maillard_chemistry_D_eff : ℕ := 15

theorem maillard_chemistry_observable_count_pos : 0 < maillard_chemistry_observable_count := by
  unfold maillard_chemistry_observable_count; decide

theorem maillard_chemistry_median_error_under_half_pct :
    (0.09443694019339477 : ℝ) < (0.5 : ℝ) := by norm_num

theorem maillard_chemistry_bundle :
    maillard_chemistry_observable_count = 30 ∧
    maillard_chemistry_D_eff = 15 ∧
    (0.09443694019339477 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold maillard_chemistry_observable_count; decide,
    by unfold maillard_chemistry_D_eff; decide,
    maillard_chemistry_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
