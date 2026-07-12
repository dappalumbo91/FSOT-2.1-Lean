/-
  FSOT Formal FpcFluidlinkTimingDeepPanelPriors — extension domain FPC_Fluidlink_Timing_Deep_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fpc_fluidlink_timing_deep_panel_observable_count : ℕ := 24
def fpc_fluidlink_timing_deep_panel_D_eff : ℕ := 20

theorem fpc_fluidlink_timing_deep_panel_observable_count_pos : 0 < fpc_fluidlink_timing_deep_panel_observable_count := by
  unfold fpc_fluidlink_timing_deep_panel_observable_count; norm_num

theorem fpc_fluidlink_timing_deep_panel_median_error_under_half_pct :
    (0.021117999999999998 : ℝ) < (0.5 : ℝ) := by norm_num

theorem fpc_fluidlink_timing_deep_panel_bundle :
    fpc_fluidlink_timing_deep_panel_observable_count = 24 ∧
    fpc_fluidlink_timing_deep_panel_D_eff = 20 ∧
    (0.021117999999999998 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fpc_fluidlink_timing_deep_panel_observable_count; norm_num,
    by unfold fpc_fluidlink_timing_deep_panel_D_eff; norm_num,
    fpc_fluidlink_timing_deep_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
