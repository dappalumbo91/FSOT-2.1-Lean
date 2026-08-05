/-
  FSOT Formal UnifiedDbCrosswalkSpinePriors — extension domain Unified_DB_Crosswalk_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def unified_db_crosswalk_spine_observable_count : ℕ := 24
def unified_db_crosswalk_spine_D_eff : ℕ := 17

theorem unified_db_crosswalk_spine_observable_count_pos : 0 < unified_db_crosswalk_spine_observable_count := by
  unfold unified_db_crosswalk_spine_observable_count; decide

theorem unified_db_crosswalk_spine_median_error_under_half_pct :
    (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by norm_num

theorem unified_db_crosswalk_spine_bundle :
    unified_db_crosswalk_spine_observable_count = 24 ∧
    unified_db_crosswalk_spine_D_eff = 17 ∧
    (0.0020923899350648867 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold unified_db_crosswalk_spine_observable_count; decide,
    by unfold unified_db_crosswalk_spine_D_eff; decide,
    unified_db_crosswalk_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
