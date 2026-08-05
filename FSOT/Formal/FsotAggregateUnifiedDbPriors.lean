/-
  FSOT Formal FsotAggregateUnifiedDbPriors — aggregate unified mathematical database.
  Generator: scripts/gen_fsot_aggregate_unified_db_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_aggregate_unified_db_observable_count : ℕ := 8
def fsot_aggregate_unified_db_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_aggregate_unified_db_D_eff : ℕ := 17

theorem fsot_aggregate_unified_db_observable_count_pos : 0 < fsot_aggregate_unified_db_observable_count := by
  unfold fsot_aggregate_unified_db_observable_count; decide

theorem fsot_aggregate_unified_db_median_error_under_five_pct :
    fsot_aggregate_unified_db_median_error_pct < (5 : ℝ) := by
  unfold fsot_aggregate_unified_db_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem fsot_aggregate_unified_db_bundle :
    fsot_aggregate_unified_db_observable_count = 8 ∧
    fsot_aggregate_unified_db_D_eff = 17 ∧
    fsot_aggregate_unified_db_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold fsot_aggregate_unified_db_observable_count; decide,
    by unfold fsot_aggregate_unified_db_D_eff; decide,
    fsot_aggregate_unified_db_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
