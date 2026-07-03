/-
  FSOT Formal MagnetosphereExtendedPriors — historical Dst×Kp + RTSW Bz + G-scale holdout.
  Generator: scripts/gen_magnetosphere_extended_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def magnetosphere_extended_historical_hours : ℕ := 120877
def magnetosphere_extended_historical_match_count : ℕ := 120627
def magnetosphere_extended_storm_holdout_hours : ℕ := 77188
def magnetosphere_extended_storm_holdout_match_count : ℕ := 76938
def magnetosphere_extended_bz_record_count : ℕ := 1416
def magnetosphere_extended_bz_match_count : ℕ := 1408
def magnetosphere_extended_D_eff : ℕ := 14
def magnetosphere_extended_historical_match_rate : ℝ := (0.9979317818939915 : ℝ)
def magnetosphere_extended_storm_holdout_match_rate : ℝ := (0.996761154583614 : ℝ)
def magnetosphere_extended_bz_match_rate : ℝ := (0.9943502824858758 : ℝ)

theorem magnetosphere_extended_historical_hours_pos : 0 < magnetosphere_extended_historical_hours := by
  unfold magnetosphere_extended_historical_hours; norm_num

theorem magnetosphere_extended_historical_match_le_total :
    magnetosphere_extended_historical_match_count ≤ magnetosphere_extended_historical_hours := by
  unfold magnetosphere_extended_historical_match_count magnetosphere_extended_historical_hours; norm_num

theorem magnetosphere_extended_storm_holdout_match_le_total :
    magnetosphere_extended_storm_holdout_match_count ≤ magnetosphere_extended_storm_holdout_hours := by
  unfold magnetosphere_extended_storm_holdout_match_count magnetosphere_extended_storm_holdout_hours; norm_num

theorem magnetosphere_extended_bz_match_le_total :
    magnetosphere_extended_bz_match_count ≤ magnetosphere_extended_bz_record_count := by
  unfold magnetosphere_extended_bz_match_count magnetosphere_extended_bz_record_count; norm_num

theorem magnetosphere_extended_bundle :
    magnetosphere_extended_historical_hours = 120877 ∧
    magnetosphere_extended_historical_match_count = 120627 ∧
    magnetosphere_extended_storm_holdout_hours = 77188 ∧
    magnetosphere_extended_storm_holdout_match_count = 76938 ∧
    magnetosphere_extended_bz_record_count = 1416 ∧
    magnetosphere_extended_bz_match_count = 1408 ∧
    magnetosphere_extended_D_eff = 14 ∧
    magnetosphere_extended_historical_match_count ≤ magnetosphere_extended_historical_hours ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold magnetosphere_extended_historical_hours; norm_num,
    by unfold magnetosphere_extended_historical_match_count; norm_num,
    by unfold magnetosphere_extended_storm_holdout_hours; norm_num,
    by unfold magnetosphere_extended_storm_holdout_match_count; norm_num,
    by unfold magnetosphere_extended_bz_record_count; norm_num,
    by unfold magnetosphere_extended_bz_match_count; norm_num,
    by unfold magnetosphere_extended_D_eff; norm_num,
    magnetosphere_extended_historical_match_le_total,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
