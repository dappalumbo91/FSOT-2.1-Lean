/-
  FSOT Formal CryospherePriors — northern climate cryosphere proxy cohort.
  Generator: scripts/gen_cryosphere_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def cryosphere_month_count : ℕ := 2399
def cryosphere_station_count : ℕ := 4
def cryosphere_match_count : ℕ := 2399
def cryosphere_D_eff : ℕ := 16
def cryosphere_match_rate : ℝ := (1.0 : ℝ)

theorem cryosphere_month_count_pos : 0 < cryosphere_month_count := by
  unfold cryosphere_month_count; norm_num

theorem cryosphere_match_le_total : cryosphere_match_count ≤ cryosphere_month_count := by
  unfold cryosphere_match_count cryosphere_month_count; norm_num

theorem cryosphere_bundle :
    cryosphere_month_count = 2399 ∧
    cryosphere_station_count = 4 ∧
    cryosphere_match_count = 2399 ∧
    cryosphere_D_eff = 16 ∧
    cryosphere_match_count ≤ cryosphere_month_count ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold cryosphere_month_count; norm_num,
    by unfold cryosphere_station_count; norm_num,
    by unfold cryosphere_match_count; norm_num,
    by unfold cryosphere_D_eff; norm_num,
    cryosphere_match_le_total,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
