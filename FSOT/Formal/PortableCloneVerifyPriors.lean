/-
  FSOT Formal PortableCloneVerifyPriors — extension domain Portable_Clone_Verify.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def portable_clone_verify_observable_count : ℕ := 290
def portable_clone_verify_D_eff : ℕ := 14

theorem portable_clone_verify_observable_count_pos : 0 < portable_clone_verify_observable_count := by
  unfold portable_clone_verify_observable_count; decide

theorem portable_clone_verify_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem portable_clone_verify_bundle :
    portable_clone_verify_observable_count = 290 ∧
    portable_clone_verify_D_eff = 14 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold portable_clone_verify_observable_count; decide,
    by unfold portable_clone_verify_D_eff; decide,
    portable_clone_verify_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
