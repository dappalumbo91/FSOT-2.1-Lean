/-
  FSOT Formal PhysarumBiologicalCudaPanelPriors — Tier 88 application wiring (Physarum_Biological_CUDA_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def biological_cuda_observable_count : ℕ := 5
def biological_cuda_median_error_pct : ℝ := (0.022236 : ℝ)
def biological_cuda_D_eff : ℕ := 15

theorem biological_cuda_observable_count_pos : 0 < biological_cuda_observable_count := by
  unfold biological_cuda_observable_count; norm_num

theorem biological_cuda_median_error_under_five_pct :
    biological_cuda_median_error_pct < (5 : ℝ) := by
  unfold biological_cuda_median_error_pct; norm_num

theorem biological_cuda_bundle :
    biological_cuda_observable_count = 5 ∧
    biological_cuda_D_eff = 15 ∧
    biological_cuda_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold biological_cuda_observable_count; norm_num,
    by unfold biological_cuda_D_eff; norm_num,
    biological_cuda_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
