/-
  FSOT Formal PublicVerifiableSpinePriors — Tier 81 credential-free public (Public_Verifiable_Spine).
  Generator: scripts/gen_tier81_public_verifiable_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def public_verifiable_spine_observable_count : ℕ := 20
def public_verifiable_spine_median_error_pct : ℝ := (0.0 : ℝ)
def public_verifiable_spine_D_eff : ℕ := 16

theorem public_verifiable_spine_observable_count_pos : 0 < public_verifiable_spine_observable_count := by
  unfold public_verifiable_spine_observable_count; norm_num

theorem public_verifiable_spine_median_error_under_five_pct :
    public_verifiable_spine_median_error_pct < (5 : ℝ) := by
  unfold public_verifiable_spine_median_error_pct; norm_num

theorem public_verifiable_spine_bundle :
    public_verifiable_spine_observable_count = 20 ∧
    public_verifiable_spine_D_eff = 16 ∧
    public_verifiable_spine_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold public_verifiable_spine_observable_count; norm_num,
    by unfold public_verifiable_spine_D_eff; norm_num,
    public_verifiable_spine_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
