/-
  FSOT Formal Esp32PlatformEngineeringPanelPriors — engineering/code residual panel (ESP32_Platform_Engineering_Panel).
  Generator: scripts/gen_engineering_code_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def esp32_platform_engineering_observable_count : ℕ := 34
def esp32_platform_engineering_median_error_pct : ℝ := (0.020755 : ℝ)
def esp32_platform_engineering_D_eff : ℕ := 12

theorem esp32_platform_engineering_observable_count_pos : 0 < esp32_platform_engineering_observable_count := by
  unfold esp32_platform_engineering_observable_count; decide

theorem esp32_platform_engineering_median_error_under_half_pct :
    esp32_platform_engineering_median_error_pct < (0.5 : ℝ) := by
  unfold esp32_platform_engineering_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem esp32_platform_engineering_bundle :
    esp32_platform_engineering_observable_count = 34 ∧
    esp32_platform_engineering_D_eff = 12 ∧
    esp32_platform_engineering_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold esp32_platform_engineering_observable_count; decide,
    by unfold esp32_platform_engineering_D_eff; decide,
    esp32_platform_engineering_median_error_under_half_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
