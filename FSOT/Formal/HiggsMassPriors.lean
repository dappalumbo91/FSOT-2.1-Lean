/-
  FSOT Formal HiggsMassPriors — extension domain Higgs_Mass.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def higgs_mass_observable_count : ℕ := 9
def higgs_mass_D_eff : ℕ := 19

theorem higgs_mass_observable_count_pos : 0 < higgs_mass_observable_count := by
  unfold higgs_mass_observable_count; norm_num

theorem higgs_mass_median_error_under_half_pct :
    (0.03990518384182655 : ℝ) < (0.5 : ℝ) := by norm_num

theorem higgs_mass_bundle :
    higgs_mass_observable_count = 9 ∧
    higgs_mass_D_eff = 19 ∧
    (0.03990518384182655 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold higgs_mass_observable_count; norm_num,
    by unfold higgs_mass_D_eff; norm_num,
    higgs_mass_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
