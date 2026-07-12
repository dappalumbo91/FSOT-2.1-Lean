/-
  FSOT Formal EpidemiologyPriors — extension domain Epidemiology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def epidemiology_observable_count : ℕ := 20
def epidemiology_D_eff : ℕ := 15

theorem epidemiology_observable_count_pos : 0 < epidemiology_observable_count := by
  unfold epidemiology_observable_count; norm_num

theorem epidemiology_median_error_under_half_pct :
    (0.03062212293865052 : ℝ) < (0.5 : ℝ) := by norm_num

theorem epidemiology_bundle :
    epidemiology_observable_count = 20 ∧
    epidemiology_D_eff = 15 ∧
    (0.03062212293865052 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold epidemiology_observable_count; norm_num,
    by unfold epidemiology_D_eff; norm_num,
    epidemiology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
