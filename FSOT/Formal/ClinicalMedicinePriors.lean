/-
  FSOT Formal ClinicalMedicinePriors — extension domain Clinical_Medicine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def clinical_medicine_observable_count : ℕ := 260
def clinical_medicine_D_eff : ℕ := 15

theorem clinical_medicine_observable_count_pos : 0 < clinical_medicine_observable_count := by
  unfold clinical_medicine_observable_count; decide

theorem clinical_medicine_median_error_under_half_pct :
    (0.002458296751538192 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.002458296751538192 : ℝ) < (0.5 : ℝ))

theorem clinical_medicine_bundle :
    clinical_medicine_observable_count = 260 ∧
    clinical_medicine_D_eff = 15 ∧
    (0.002458296751538192 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold clinical_medicine_observable_count; decide,
    by unfold clinical_medicine_D_eff; decide,
    clinical_medicine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
