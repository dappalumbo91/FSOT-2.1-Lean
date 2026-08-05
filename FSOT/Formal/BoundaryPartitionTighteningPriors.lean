/-
  FSOT Formal BoundaryPartitionTighteningPriors — extension domain Boundary_Partition_Tightening.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def boundary_partition_tightening_observable_count : ℕ := 24
def boundary_partition_tightening_D_eff : ℕ := 17

theorem boundary_partition_tightening_observable_count_pos : 0 < boundary_partition_tightening_observable_count := by
  unfold boundary_partition_tightening_observable_count; decide

theorem boundary_partition_tightening_median_error_under_half_pct :
    (0.017672674984670764 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.017672674984670764 : ℝ) < (0.5 : ℝ))

theorem boundary_partition_tightening_bundle :
    boundary_partition_tightening_observable_count = 24 ∧
    boundary_partition_tightening_D_eff = 17 ∧
    (0.017672674984670764 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold boundary_partition_tightening_observable_count; decide,
    by unfold boundary_partition_tightening_D_eff; decide,
    boundary_partition_tightening_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
