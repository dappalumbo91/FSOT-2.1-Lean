/-
  FSOT Formal BlackHoleWhiteholeCycleLivePanelPriors — Tier 88 application wiring (BlackHole_WhiteHole_Cycle_Live_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def blackhole_whitehole_cycle_observable_count : ℕ := 11
def blackhole_whitehole_cycle_median_error_pct : ℝ := (0.026472 : ℝ)
def blackhole_whitehole_cycle_D_eff : ℕ := 18

theorem blackhole_whitehole_cycle_observable_count_pos : 0 < blackhole_whitehole_cycle_observable_count := by
  unfold blackhole_whitehole_cycle_observable_count; norm_num

theorem blackhole_whitehole_cycle_median_error_under_five_pct :
    blackhole_whitehole_cycle_median_error_pct < (5 : ℝ) := by
  unfold blackhole_whitehole_cycle_median_error_pct; norm_num

theorem blackhole_whitehole_cycle_bundle :
    blackhole_whitehole_cycle_observable_count = 11 ∧
    blackhole_whitehole_cycle_D_eff = 18 ∧
    blackhole_whitehole_cycle_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "blackhole") > 0 := by
  refine ⟨
    by unfold blackhole_whitehole_cycle_observable_count; norm_num,
    by unfold blackhole_whitehole_cycle_D_eff; norm_num,
    blackhole_whitehole_cycle_median_error_under_five_pct,
    blackhole_raw_S_positive
  ⟩

end

end FSOT.Formal
