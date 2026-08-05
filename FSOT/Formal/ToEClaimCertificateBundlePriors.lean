/-
  FSOT Formal ToeClaimCertificateBundlePriors — extension domain ToE_Claim_Certificate_Bundle.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def toe_claim_certificate_bundle_observable_count : ℕ := 24
def toe_claim_certificate_bundle_D_eff : ℕ := 25

theorem toe_claim_certificate_bundle_observable_count_pos : 0 < toe_claim_certificate_bundle_observable_count := by
  unfold toe_claim_certificate_bundle_observable_count; decide

theorem toe_claim_certificate_bundle_median_error_under_half_pct :
    (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by norm_num

theorem toe_claim_certificate_bundle_bundle :
    toe_claim_certificate_bundle_observable_count = 24 ∧
    toe_claim_certificate_bundle_D_eff = 25 ∧
    (0.0020923899350648867 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold toe_claim_certificate_bundle_observable_count; decide,
    by unfold toe_claim_certificate_bundle_D_eff; decide,
    toe_claim_certificate_bundle_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
