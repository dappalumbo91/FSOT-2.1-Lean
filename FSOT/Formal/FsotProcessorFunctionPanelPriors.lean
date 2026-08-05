/-
  FSOT Formal FsotProcessorFunctionPanelPriors — GPU/CUDA/processor/RAM seed residual panel (FSOT_Processor_Function_Panel).
  Generator: scripts/gen_fsot_gpu_cuda_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_processor_function_observable_count : ℕ := 20
def fsot_processor_function_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_processor_function_D_eff : ℕ := 12

theorem fsot_processor_function_observable_count_pos : 0 < fsot_processor_function_observable_count := by
  unfold fsot_processor_function_observable_count; decide

theorem fsot_processor_function_median_error_under_half_pct :
    fsot_processor_function_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_processor_function_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem fsot_processor_function_bundle :
    fsot_processor_function_observable_count = 20 ∧
    fsot_processor_function_D_eff = 12 ∧
    fsot_processor_function_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fsot_processor_function_observable_count; decide,
    by unfold fsot_processor_function_D_eff; decide,
    fsot_processor_function_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
