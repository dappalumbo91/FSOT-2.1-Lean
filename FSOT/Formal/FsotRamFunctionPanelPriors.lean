/-
  FSOT Formal FsotRamFunctionPanelPriors — GPU/CUDA/processor/RAM seed residual panel (FSOT_RAM_Function_Panel).
  Generator: scripts/gen_fsot_gpu_cuda_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_ram_function_observable_count : ℕ := 33
def fsot_ram_function_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_ram_function_D_eff : ℕ := 11

theorem fsot_ram_function_observable_count_pos : 0 < fsot_ram_function_observable_count := by
  unfold fsot_ram_function_observable_count; decide

theorem fsot_ram_function_median_error_under_half_pct :
    fsot_ram_function_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_ram_function_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem fsot_ram_function_bundle :
    fsot_ram_function_observable_count = 33 ∧
    fsot_ram_function_D_eff = 11 ∧
    fsot_ram_function_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold fsot_ram_function_observable_count; decide,
    by unfold fsot_ram_function_D_eff; decide,
    fsot_ram_function_median_error_under_half_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
