/-
  FSOT Formal VlDistillAtlasPriors — VL distill atlas + domain registry crosswalk.
  Generator: scripts/gen_vl_distill_atlas_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def vl_distill_atlas_observable_count : ℕ := 10
def vl_distill_atlas_median_error_pct : ℝ := (0.0 : ℝ)
def vl_distill_atlas_D_eff : ℕ := 12

theorem vl_distill_atlas_observable_count_pos : 0 < vl_distill_atlas_observable_count := by
  unfold vl_distill_atlas_observable_count; norm_num

theorem vl_distill_atlas_median_error_under_half_pct :
    vl_distill_atlas_median_error_pct < (0.5 : ℝ) := by
  unfold vl_distill_atlas_median_error_pct; norm_num

theorem vl_distill_atlas_bundle :
    vl_distill_atlas_observable_count = 10 ∧
    vl_distill_atlas_D_eff = 12 ∧
    vl_distill_atlas_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold vl_distill_atlas_observable_count; norm_num,
    by unfold vl_distill_atlas_D_eff; norm_num,
    vl_distill_atlas_median_error_under_half_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
