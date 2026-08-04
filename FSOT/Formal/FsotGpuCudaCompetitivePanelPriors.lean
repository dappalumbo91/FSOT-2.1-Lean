/-
  FSOT Formal FsotGpuCudaCompetitivePanelPriors — GPU/CUDA/processor/RAM seed residual panel (FSOT_GPU_CUDA_Competitive_Panel).
  Generator: scripts/gen_fsot_gpu_cuda_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_gpu_cuda_competitive_observable_count : ℕ := 33
def fsot_gpu_cuda_competitive_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_gpu_cuda_competitive_D_eff : ℕ := 12

theorem fsot_gpu_cuda_competitive_observable_count_pos : 0 < fsot_gpu_cuda_competitive_observable_count := by
  unfold fsot_gpu_cuda_competitive_observable_count; norm_num

theorem fsot_gpu_cuda_competitive_median_error_under_half_pct :
    fsot_gpu_cuda_competitive_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_gpu_cuda_competitive_median_error_pct; norm_num

theorem fsot_gpu_cuda_competitive_bundle :
    fsot_gpu_cuda_competitive_observable_count = 33 ∧
    fsot_gpu_cuda_competitive_D_eff = 12 ∧
    fsot_gpu_cuda_competitive_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "quantum") > 0 := by
  refine ⟨
    by unfold fsot_gpu_cuda_competitive_observable_count; norm_num,
    by unfold fsot_gpu_cuda_competitive_D_eff; norm_num,
    fsot_gpu_cuda_competitive_median_error_under_half_pct,
    quantum_raw_S_positive
  ⟩

end

end FSOT.Formal
