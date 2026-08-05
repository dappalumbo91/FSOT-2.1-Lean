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
  unfold vl_distill_atlas_observable_count; decide

theorem vl_distill_atlas_median_error_under_five_pct :
    vl_distill_atlas_median_error_pct < (5 : ℝ) := by
  unfold vl_distill_atlas_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem vl_distill_atlas_bundle :
    vl_distill_atlas_observable_count = 10 ∧
    vl_distill_atlas_D_eff = 12 ∧
    vl_distill_atlas_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold vl_distill_atlas_observable_count; decide,
    by unfold vl_distill_atlas_D_eff; decide,
    vl_distill_atlas_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
