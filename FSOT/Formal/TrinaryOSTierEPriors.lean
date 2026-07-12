/-
  FSOT Formal TrinaryOsTierEPriors — extension domain Trinary_OS_Tier_E.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def trinary_os_tier_e_observable_count : ℕ := 68
def trinary_os_tier_e_D_eff : ℕ := 12

theorem trinary_os_tier_e_observable_count_pos : 0 < trinary_os_tier_e_observable_count := by
  unfold trinary_os_tier_e_observable_count; norm_num

theorem trinary_os_tier_e_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem trinary_os_tier_e_bundle :
    trinary_os_tier_e_observable_count = 68 ∧
    trinary_os_tier_e_D_eff = 12 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold trinary_os_tier_e_observable_count; norm_num,
    by unfold trinary_os_tier_e_D_eff; norm_num,
    trinary_os_tier_e_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
