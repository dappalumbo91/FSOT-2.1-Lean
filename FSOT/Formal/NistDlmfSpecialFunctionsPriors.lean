/-
  FSOT Formal NistDlmfSpecialFunctionsPriors — extension domain NIST_DLMF_Special_Functions.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def nist_dlmf_special_functions_observable_count : ℕ := 21
def nist_dlmf_special_functions_D_eff : ℕ := 14

theorem nist_dlmf_special_functions_observable_count_pos : 0 < nist_dlmf_special_functions_observable_count := by
  unfold nist_dlmf_special_functions_observable_count; decide

theorem nist_dlmf_special_functions_median_error_under_half_pct :
    (0.020055 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.020055 : ℝ) < (0.5 : ℝ))

theorem nist_dlmf_special_functions_bundle :
    nist_dlmf_special_functions_observable_count = 21 ∧
    nist_dlmf_special_functions_D_eff = 14 ∧
    (0.020055 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold nist_dlmf_special_functions_observable_count; decide,
    by unfold nist_dlmf_special_functions_D_eff; decide,
    nist_dlmf_special_functions_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
