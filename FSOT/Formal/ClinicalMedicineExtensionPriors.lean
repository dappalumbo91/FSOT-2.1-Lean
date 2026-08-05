/-
  FSOT Formal ClinicalMedicineExtensionPriors — Clinical_Medicine Tier D extension (real API anchors).
  Generator: scripts/gen_tier_d_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def clinical_medicine_ext_observable_count : ℕ := 260
def clinical_medicine_ext_pooled_median_error_pct : ℝ := (0.0029447130131637534 : ℝ)
def clinical_medicine_ext_headline_median_error_pct : ℝ := (0.0029447130131637534 : ℝ)
def clinical_medicine_ext_beats_sota_headlines : ℕ := 2
def clinical_medicine_ext_D_eff : ℕ := 15

theorem clinical_medicine_ext_observable_count_pos : 0 < clinical_medicine_ext_observable_count := by
  unfold clinical_medicine_ext_observable_count; decide

theorem clinical_medicine_ext_pooled_median_under_half_pct :
    clinical_medicine_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold clinical_medicine_ext_pooled_median_error_pct
  exact (by norm_num : (0.0029447130131637534  : ℝ) < 0.5)

theorem clinical_medicine_ext_headline_median_under_half_pct :
    clinical_medicine_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold clinical_medicine_ext_headline_median_error_pct
  exact (by norm_num : (0.0029447130131637534  : ℝ) < 0.5)

theorem clinical_medicine_ext_beats_sota_headlines_pos : 0 < clinical_medicine_ext_beats_sota_headlines := by
  unfold clinical_medicine_ext_beats_sota_headlines; decide

theorem clinical_medicine_ext_bundle :
    clinical_medicine_ext_observable_count = 260 ∧
    clinical_medicine_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    clinical_medicine_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < clinical_medicine_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold clinical_medicine_ext_observable_count; decide,
    clinical_medicine_ext_pooled_median_under_half_pct,
    clinical_medicine_ext_headline_median_under_half_pct,
    clinical_medicine_ext_beats_sota_headlines_pos,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
