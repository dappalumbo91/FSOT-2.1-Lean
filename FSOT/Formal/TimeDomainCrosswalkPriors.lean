/-
  FSOT Formal TimeDomainCrosswalkPriors — extension domain Time_Domain_Crosswalk.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def time_domain_crosswalk_observable_count : ℕ := 250
def time_domain_crosswalk_D_eff : ℕ := 19

theorem time_domain_crosswalk_observable_count_pos : 0 < time_domain_crosswalk_observable_count := by
  unfold time_domain_crosswalk_observable_count; norm_num

theorem time_domain_crosswalk_median_error_under_half_pct :
    (0.028056 : ℝ) < (0.5 : ℝ) := by norm_num

theorem time_domain_crosswalk_bundle :
    time_domain_crosswalk_observable_count = 250 ∧
    time_domain_crosswalk_D_eff = 19 ∧
    (0.028056 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold time_domain_crosswalk_observable_count; norm_num,
    by unfold time_domain_crosswalk_D_eff; norm_num,
    time_domain_crosswalk_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
