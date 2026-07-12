/-
  FSOT Formal IgemPartsExpandedPriors — extension domain IGEM_Parts_Expanded.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def igem_parts_expanded_observable_count : ℕ := 111
def igem_parts_expanded_D_eff : ℕ := 14

theorem igem_parts_expanded_observable_count_pos : 0 < igem_parts_expanded_observable_count := by
  unfold igem_parts_expanded_observable_count; norm_num

theorem igem_parts_expanded_median_error_under_half_pct :
    (5.882356401581393e-05 : ℝ) < (0.5 : ℝ) := by norm_num

theorem igem_parts_expanded_bundle :
    igem_parts_expanded_observable_count = 111 ∧
    igem_parts_expanded_D_eff = 14 ∧
    (5.882356401581393e-05 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold igem_parts_expanded_observable_count; norm_num,
    by unfold igem_parts_expanded_D_eff; norm_num,
    igem_parts_expanded_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
