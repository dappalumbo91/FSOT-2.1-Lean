/-
  FSOT Formal NistCodataConstantsPriors — Tier 38 public API (NIST_CODATA_Constants).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def nist_codata_constants_observable_count : ℕ := 6
def nist_codata_constants_median_error_pct : ℝ := (0.0 : ℝ)
def nist_codata_constants_D_eff : ℕ := 7

theorem nist_codata_constants_observable_count_pos : 0 < nist_codata_constants_observable_count := by
  unfold nist_codata_constants_observable_count; decide

theorem nist_codata_constants_median_error_under_five_pct :
    nist_codata_constants_median_error_pct < (5 : ℝ) := by
  unfold nist_codata_constants_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem nist_codata_constants_bundle :
    nist_codata_constants_observable_count = 6 ∧
    nist_codata_constants_D_eff = 7 ∧
    nist_codata_constants_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold nist_codata_constants_observable_count; decide,
    by unfold nist_codata_constants_D_eff; decide,
    nist_codata_constants_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
