/-
  FSOT Formal ClinicaltrialsMedicalPriors — Tier 80 government open data (ClinicalTrials_Medical_Panel).
  Generator: scripts/gen_tier80_government_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def clinicaltrials_medical_observable_count : ℕ := 394
def clinicaltrials_medical_median_error_pct : ℝ := (0.0 : ℝ)
def clinicaltrials_medical_D_eff : ℕ := 13

theorem clinicaltrials_medical_observable_count_pos : 0 < clinicaltrials_medical_observable_count := by
  unfold clinicaltrials_medical_observable_count; decide

theorem clinicaltrials_medical_median_error_under_five_pct :
    clinicaltrials_medical_median_error_pct < (5 : ℝ) := by
  unfold clinicaltrials_medical_median_error_pct; norm_num

theorem clinicaltrials_medical_bundle :
    clinicaltrials_medical_observable_count = 394 ∧
    clinicaltrials_medical_D_eff = 13 ∧
    clinicaltrials_medical_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold clinicaltrials_medical_observable_count; decide,
    by unfold clinicaltrials_medical_D_eff; decide,
    clinicaltrials_medical_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
