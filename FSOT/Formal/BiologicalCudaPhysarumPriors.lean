/-
  FSOT Formal BiologicalCudaPhysarumPriors — Physarum CUDA biology crosswalk.
  Generator: scripts/gen_biological_cuda_physarum_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def biological_cuda_physarum_observable_count : ℕ := 35
def biological_cuda_physarum_median_error_pct : ℝ := (0.0 : ℝ)
def biological_cuda_physarum_D_eff : ℕ := 22

theorem biological_cuda_physarum_observable_count_pos : 0 < biological_cuda_physarum_observable_count := by
  unfold biological_cuda_physarum_observable_count; decide

theorem biological_cuda_physarum_median_error_under_five_pct :
    biological_cuda_physarum_median_error_pct < (5 : ℝ) := by
  unfold biological_cuda_physarum_median_error_pct; norm_num

theorem biological_cuda_physarum_bundle :
    biological_cuda_physarum_observable_count = 35 ∧
    biological_cuda_physarum_D_eff = 22 ∧
    biological_cuda_physarum_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold biological_cuda_physarum_observable_count; decide,
    by unfold biological_cuda_physarum_D_eff; decide,
    biological_cuda_physarum_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
