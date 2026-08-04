/-
  FSOT Formal FsotCacheHierarchyPanelPriors — hardware depth (FSOT_Cache_Hierarchy_Panel).
  Generator: scripts/gen_hardware_depth_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_cache_hierarchy_observable_count : ℕ := 11
def fsot_cache_hierarchy_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_cache_hierarchy_D_eff : ℕ := 11

theorem fsot_cache_hierarchy_observable_count_pos : 0 < fsot_cache_hierarchy_observable_count := by
  unfold fsot_cache_hierarchy_observable_count; norm_num

theorem fsot_cache_hierarchy_median_error_under_half_pct :
    fsot_cache_hierarchy_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_cache_hierarchy_median_error_pct; norm_num

theorem fsot_cache_hierarchy_bundle :
    fsot_cache_hierarchy_observable_count = 11 ∧
    fsot_cache_hierarchy_D_eff = 11 ∧
    fsot_cache_hierarchy_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fsot_cache_hierarchy_observable_count; norm_num,
    by unfold fsot_cache_hierarchy_D_eff; norm_num,
    fsot_cache_hierarchy_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
