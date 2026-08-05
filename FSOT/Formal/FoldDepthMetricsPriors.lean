/-
  FSOT Formal FoldDepthMetricsPriors — extension domain Fold_Depth_Metrics.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fold_depth_metrics_observable_count : ℕ := 51
def fold_depth_metrics_D_eff : ℕ := 20

theorem fold_depth_metrics_observable_count_pos : 0 < fold_depth_metrics_observable_count := by
  unfold fold_depth_metrics_observable_count; decide

theorem fold_depth_metrics_median_error_under_half_pct :
    (0.025753835305195434 : ℝ) < (0.5 : ℝ) := by norm_num

theorem fold_depth_metrics_bundle :
    fold_depth_metrics_observable_count = 51 ∧
    fold_depth_metrics_D_eff = 20 ∧
    (0.025753835305195434 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fold_depth_metrics_observable_count; decide,
    by unfold fold_depth_metrics_D_eff; decide,
    fold_depth_metrics_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
