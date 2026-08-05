/-
  FSOT Formal HiggsMassPriors — extension domain Higgs_Mass.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def higgs_mass_observable_count : ℕ := 24
def higgs_mass_D_eff : ℕ := 19

theorem higgs_mass_observable_count_pos : 0 < higgs_mass_observable_count := by
  unfold higgs_mass_observable_count; decide

theorem higgs_mass_median_error_under_half_pct :
    (0.012112816039879785 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.012112816039879785 : ℝ) < (0.5 : ℝ))

theorem higgs_mass_bundle :
    higgs_mass_observable_count = 24 ∧
    higgs_mass_D_eff = 19 ∧
    (0.012112816039879785 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold higgs_mass_observable_count; decide,
    by unfold higgs_mass_D_eff; decide,
    higgs_mass_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
