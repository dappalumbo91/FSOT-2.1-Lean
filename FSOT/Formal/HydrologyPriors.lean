/-
  FSOT Formal HydrologyPriors — USGS streamflow anomaly classifier.
  Generator: scripts/gen_hydrology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def hydrology_month_count : ℕ := 960
def hydrology_station_count : ℕ := 8
def hydrology_stability_match_count : ℕ := 957
def hydrology_D_eff : ℕ := 15
def hydrology_stability_match_rate : ℝ := (0.996875 : ℝ)

theorem hydrology_month_count_pos : 0 < hydrology_month_count := by
  unfold hydrology_month_count; norm_num

theorem hydrology_stability_match_le_total :
    hydrology_stability_match_count ≤ hydrology_month_count := by
  unfold hydrology_stability_match_count hydrology_month_count; norm_num

theorem hydrology_stability_match_rate_nonneg : (0 : ℝ) ≤ hydrology_stability_match_rate := by
  unfold hydrology_stability_match_rate; norm_num

theorem hydrology_bundle :
    hydrology_month_count = 960 ∧
    hydrology_station_count = 8 ∧
    hydrology_stability_match_count = 957 ∧
    hydrology_D_eff = 15 ∧
    hydrology_stability_match_count ≤ hydrology_month_count ∧
    (0 : ℝ) ≤ hydrology_stability_match_rate ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold hydrology_month_count; norm_num,
    by unfold hydrology_station_count; norm_num,
    by unfold hydrology_stability_match_count; norm_num,
    by unfold hydrology_D_eff; norm_num,
    hydrology_stability_match_le_total,
    hydrology_stability_match_rate_nonneg,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
