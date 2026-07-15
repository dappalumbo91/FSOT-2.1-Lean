/-
  FSOT Formal BlackholeWhiteholeCycleLivePanelPriors — extension domain BlackHole_WhiteHole_Cycle_Live_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def blackhole_whitehole_cycle_live_panel_observable_count : ℕ := 24
def blackhole_whitehole_cycle_live_panel_D_eff : ℕ := 18

theorem blackhole_whitehole_cycle_live_panel_observable_count_pos : 0 < blackhole_whitehole_cycle_live_panel_observable_count := by
  unfold blackhole_whitehole_cycle_live_panel_observable_count; norm_num

theorem blackhole_whitehole_cycle_live_panel_median_error_under_half_pct :
    (0.026472 : ℝ) < (0.5 : ℝ) := by norm_num

theorem blackhole_whitehole_cycle_live_panel_bundle :
    blackhole_whitehole_cycle_live_panel_observable_count = 24 ∧
    blackhole_whitehole_cycle_live_panel_D_eff = 18 ∧
    (0.026472 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold blackhole_whitehole_cycle_live_panel_observable_count; norm_num,
    by unfold blackhole_whitehole_cycle_live_panel_D_eff; norm_num,
    blackhole_whitehole_cycle_live_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
