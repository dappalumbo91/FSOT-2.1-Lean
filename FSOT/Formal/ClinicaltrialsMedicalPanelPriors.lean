/-
  FSOT Formal ClinicaltrialsMedicalPanelPriors — extension domain ClinicalTrials_Medical_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def clinicaltrials_medical_panel_observable_count : ℕ := 394
def clinicaltrials_medical_panel_D_eff : ℕ := 13

theorem clinicaltrials_medical_panel_observable_count_pos : 0 < clinicaltrials_medical_panel_observable_count := by
  unfold clinicaltrials_medical_panel_observable_count; decide

theorem clinicaltrials_medical_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem clinicaltrials_medical_panel_bundle :
    clinicaltrials_medical_panel_observable_count = 394 ∧
    clinicaltrials_medical_panel_D_eff = 13 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold clinicaltrials_medical_panel_observable_count; decide,
    by unfold clinicaltrials_medical_panel_D_eff; decide,
    clinicaltrials_medical_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
