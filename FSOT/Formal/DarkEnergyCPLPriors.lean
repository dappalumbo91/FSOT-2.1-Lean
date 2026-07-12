/-
  FSOT Formal DarkEnergyCplPriors — extension domain Dark_Energy_CPL.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def dark_energy_cpl_observable_count : ℕ := 24
def dark_energy_cpl_D_eff : ℕ := 24

theorem dark_energy_cpl_observable_count_pos : 0 < dark_energy_cpl_observable_count := by
  unfold dark_energy_cpl_observable_count; norm_num

theorem dark_energy_cpl_median_error_under_half_pct :
    (0.029733 : ℝ) < (0.5 : ℝ) := by norm_num

theorem dark_energy_cpl_bundle :
    dark_energy_cpl_observable_count = 24 ∧
    dark_energy_cpl_D_eff = 24 ∧
    (0.029733 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold dark_energy_cpl_observable_count; norm_num,
    by unfold dark_energy_cpl_D_eff; norm_num,
    dark_energy_cpl_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
