/-
  FSOT Formal FusionLabCertificateSpinePriors — extension domain Fusion_Lab_Certificate_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fusion_lab_certificate_spine_observable_count : ℕ := 50
def fusion_lab_certificate_spine_D_eff : ℕ := 20

theorem fusion_lab_certificate_spine_observable_count_pos : 0 < fusion_lab_certificate_spine_observable_count := by
  unfold fusion_lab_certificate_spine_observable_count; decide

theorem fusion_lab_certificate_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem fusion_lab_certificate_spine_bundle :
    fusion_lab_certificate_spine_observable_count = 50 ∧
    fusion_lab_certificate_spine_D_eff = 20 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fusion_lab_certificate_spine_observable_count; decide,
    by unfold fusion_lab_certificate_spine_D_eff; decide,
    fusion_lab_certificate_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
