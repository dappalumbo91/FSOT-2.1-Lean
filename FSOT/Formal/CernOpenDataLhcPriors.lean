/-
  FSOT Formal CernOpenDataLhcPriors — Tier 38 public API (CERN_Open_Data_LHC).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def cern_open_data_lhc_observable_count : ℕ := 83
def cern_open_data_lhc_median_error_pct : ℝ := (0.0 : ℝ)
def cern_open_data_lhc_D_eff : ℕ := 19

theorem cern_open_data_lhc_observable_count_pos : 0 < cern_open_data_lhc_observable_count := by
  unfold cern_open_data_lhc_observable_count; norm_num

theorem cern_open_data_lhc_median_error_under_five_pct :
    cern_open_data_lhc_median_error_pct < (5 : ℝ) := by
  unfold cern_open_data_lhc_median_error_pct; norm_num

theorem cern_open_data_lhc_bundle :
    cern_open_data_lhc_observable_count = 83 ∧
    cern_open_data_lhc_D_eff = 19 ∧
    cern_open_data_lhc_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold cern_open_data_lhc_observable_count; norm_num,
    by unfold cern_open_data_lhc_D_eff; norm_num,
    cern_open_data_lhc_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
