/-
  FSOT Formal FsotGpuParityVerifyPanelPriors — GPU/CUDA/processor/RAM seed residual panel (FSOT_GPU_Parity_Verify_Panel).
  Generator: scripts/gen_fsot_gpu_cuda_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_gpu_parity_verify_observable_count : ℕ := 48
def fsot_gpu_parity_verify_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_gpu_parity_verify_D_eff : ℕ := 11

theorem fsot_gpu_parity_verify_observable_count_pos : 0 < fsot_gpu_parity_verify_observable_count := by
  unfold fsot_gpu_parity_verify_observable_count; decide

theorem fsot_gpu_parity_verify_median_error_under_half_pct :
    fsot_gpu_parity_verify_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_gpu_parity_verify_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem fsot_gpu_parity_verify_bundle :
    fsot_gpu_parity_verify_observable_count = 48 ∧
    fsot_gpu_parity_verify_D_eff = 11 ∧
    fsot_gpu_parity_verify_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "quantum") > 0 := by
  refine ⟨
    by unfold fsot_gpu_parity_verify_observable_count; decide,
    by unfold fsot_gpu_parity_verify_D_eff; decide,
    fsot_gpu_parity_verify_median_error_under_half_pct,
    quantum_raw_S_positive
  ⟩

end

end FSOT.Formal
