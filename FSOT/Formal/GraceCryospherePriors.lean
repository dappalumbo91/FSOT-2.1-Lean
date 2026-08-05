/-
  FSOT Formal GraceCryospherePriors — GRACE Greenland mass-decline classifier.
  Generator: scripts/gen_grace_cryosphere_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def grace_cryosphere_month_count : ℕ := 253
def grace_cryosphere_match_count : ℕ := 253
def grace_cryosphere_D_eff : ℕ := 16
def grace_cryosphere_match_rate : ℝ := (1.0 : ℝ)

theorem grace_cryosphere_month_count_pos : 0 < grace_cryosphere_month_count := by
  unfold grace_cryosphere_month_count; decide

theorem grace_cryosphere_match_le_total : grace_cryosphere_match_count ≤ grace_cryosphere_month_count := by
  unfold grace_cryosphere_match_count grace_cryosphere_month_count; norm_num

theorem grace_cryosphere_bundle :
    grace_cryosphere_month_count = 253 ∧
    grace_cryosphere_match_count = 253 ∧
    grace_cryosphere_D_eff = 16 ∧
    grace_cryosphere_match_count ≤ grace_cryosphere_month_count ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold grace_cryosphere_month_count; decide,
    by unfold grace_cryosphere_match_count; decide,
    by unfold grace_cryosphere_D_eff; decide,
    grace_cryosphere_match_le_total,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
