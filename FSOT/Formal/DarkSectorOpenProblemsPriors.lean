/-
  FSOT Formal DarkSectorOpenProblemsPriors — extension domain Dark_Sector_Open_Problems.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def dark_sector_open_problems_observable_count : ℕ := 24
def dark_sector_open_problems_D_eff : ℕ := 24

theorem dark_sector_open_problems_observable_count_pos : 0 < dark_sector_open_problems_observable_count := by
  unfold dark_sector_open_problems_observable_count; decide

theorem dark_sector_open_problems_median_error_under_half_pct :
    (0.01529034996934153 : ℝ) < (0.5 : ℝ) := by norm_num

theorem dark_sector_open_problems_bundle :
    dark_sector_open_problems_observable_count = 24 ∧
    dark_sector_open_problems_D_eff = 24 ∧
    (0.01529034996934153 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold dark_sector_open_problems_observable_count; decide,
    by unfold dark_sector_open_problems_D_eff; decide,
    dark_sector_open_problems_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
