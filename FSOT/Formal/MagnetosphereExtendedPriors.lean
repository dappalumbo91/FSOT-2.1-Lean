/-
  FSOT Formal MagnetosphereExtendedPriors — historical Dst×Kp + RTSW Bz + G-scale holdout.
  Generator: scripts/gen_magnetosphere_extended_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def magnetosphere_extended_historical_hours : ℕ := 120879
def magnetosphere_extended_historical_match_count : ℕ := 120879
def magnetosphere_extended_storm_holdout_hours : ℕ := 91464
def magnetosphere_extended_storm_holdout_match_count : ℕ := 91464
def magnetosphere_extended_bz_record_count : ℕ := 1436
def magnetosphere_extended_bz_match_count : ℕ := 1436
def magnetosphere_extended_D_eff : ℕ := 14
def magnetosphere_extended_historical_match_rate : ℝ := (1.0 : ℝ)
def magnetosphere_extended_storm_holdout_match_rate : ℝ := (1.0 : ℝ)
def magnetosphere_extended_bz_match_rate : ℝ := (1.0 : ℝ)
def magnetosphere_extended_pooled_match_rate : ℝ := (1.0 : ℝ)
def magnetosphere_extended_pooled_misclassification_pct : ℝ := (0.0 : ℝ)
def magnetosphere_extended_historical_misclassification_pct : ℝ := (0.0 : ℝ)
def magnetosphere_extended_storm_holdout_misclassification_pct : ℝ := (0.0 : ℝ)
def magnetosphere_extended_bz_misclassification_pct : ℝ := (0.0 : ℝ)

theorem magnetosphere_extended_historical_hours_pos : 0 < magnetosphere_extended_historical_hours := by
  unfold magnetosphere_extended_historical_hours; decide

theorem magnetosphere_extended_historical_match_le_total :
    magnetosphere_extended_historical_match_count ≤ magnetosphere_extended_historical_hours := by
  unfold magnetosphere_extended_historical_match_count magnetosphere_extended_historical_hours; decide

theorem magnetosphere_extended_storm_holdout_match_le_total :
    magnetosphere_extended_storm_holdout_match_count ≤ magnetosphere_extended_storm_holdout_hours := by
  unfold magnetosphere_extended_storm_holdout_match_count magnetosphere_extended_storm_holdout_hours; decide

theorem magnetosphere_extended_bz_match_le_total :
    magnetosphere_extended_bz_match_count ≤ magnetosphere_extended_bz_record_count := by
  unfold magnetosphere_extended_bz_match_count magnetosphere_extended_bz_record_count; decide

theorem magnetosphere_extended_bundle :
    magnetosphere_extended_historical_hours = 120879 ∧
    magnetosphere_extended_historical_match_count = 120879 ∧
    magnetosphere_extended_storm_holdout_hours = 91464 ∧
    magnetosphere_extended_storm_holdout_match_count = 91464 ∧
    magnetosphere_extended_bz_record_count = 1436 ∧
    magnetosphere_extended_bz_match_count = 1436 ∧
    magnetosphere_extended_D_eff = 14 ∧
    magnetosphere_extended_historical_match_count ≤ magnetosphere_extended_historical_hours ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold magnetosphere_extended_historical_hours; decide,
    by unfold magnetosphere_extended_historical_match_count; decide,
    by unfold magnetosphere_extended_storm_holdout_hours; decide,
    by unfold magnetosphere_extended_storm_holdout_match_count; decide,
    by unfold magnetosphere_extended_bz_record_count; decide,
    by unfold magnetosphere_extended_bz_match_count; decide,
    by unfold magnetosphere_extended_D_eff; decide,
    magnetosphere_extended_historical_match_le_total,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
