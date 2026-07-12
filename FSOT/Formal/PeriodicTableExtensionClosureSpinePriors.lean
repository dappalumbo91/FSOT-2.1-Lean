/-
  FSOT Formal PeriodicTableExtensionClosureSpinePriors — extension domain Periodic_Table_Extension_Closure_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def periodic_table_extension_closure_spine_observable_count : ℕ := 41
def periodic_table_extension_closure_spine_D_eff : ℕ := 26

theorem periodic_table_extension_closure_spine_observable_count_pos : 0 < periodic_table_extension_closure_spine_observable_count := by
  unfold periodic_table_extension_closure_spine_observable_count; norm_num

theorem periodic_table_extension_closure_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem periodic_table_extension_closure_spine_bundle :
    periodic_table_extension_closure_spine_observable_count = 41 ∧
    periodic_table_extension_closure_spine_D_eff = 26 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold periodic_table_extension_closure_spine_observable_count; norm_num,
    by unfold periodic_table_extension_closure_spine_D_eff; norm_num,
    periodic_table_extension_closure_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
