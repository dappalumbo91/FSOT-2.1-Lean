/-
  FSOT Formal NistDlmfSpecialFunctionsPriors — reference anchor (NIST_DLMF_Special_Functions).
  Generator: scripts/gen_reference_anchors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def nist_dlmf_special_functions_observable_count : ℕ := 5
def nist_dlmf_special_functions_median_error_pct : ℝ := (0.001661 : ℝ)
def nist_dlmf_special_functions_D_eff : ℕ := 14

theorem nist_dlmf_special_functions_observable_count_pos : 0 < nist_dlmf_special_functions_observable_count := by
  unfold nist_dlmf_special_functions_observable_count; norm_num

theorem nist_dlmf_special_functions_median_error_under_five_pct :
    nist_dlmf_special_functions_median_error_pct < (5 : ℝ) := by
  unfold nist_dlmf_special_functions_median_error_pct; norm_num

theorem nist_dlmf_special_functions_bundle :
    nist_dlmf_special_functions_observable_count = 5 ∧
    nist_dlmf_special_functions_D_eff = 14 ∧
    nist_dlmf_special_functions_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold nist_dlmf_special_functions_observable_count; norm_num,
    by unfold nist_dlmf_special_functions_D_eff; norm_num,
    nist_dlmf_special_functions_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
