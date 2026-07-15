/-
  FSOT Formal TrinaryHardwareLivePanelPriors — Tier 88 application wiring (Trinary_Hardware_Live_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def trinary_hardware_live_observable_count : ℕ := 37
def trinary_hardware_live_median_error_pct : ℝ := (0.014767 : ℝ)
def trinary_hardware_live_D_eff : ℕ := 14

theorem trinary_hardware_live_observable_count_pos : 0 < trinary_hardware_live_observable_count := by
  unfold trinary_hardware_live_observable_count; norm_num

theorem trinary_hardware_live_median_error_under_five_pct :
    trinary_hardware_live_median_error_pct < (5 : ℝ) := by
  unfold trinary_hardware_live_median_error_pct; norm_num

theorem trinary_hardware_live_bundle :
    trinary_hardware_live_observable_count = 37 ∧
    trinary_hardware_live_D_eff = 14 ∧
    trinary_hardware_live_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "ai") > 0 := by
  refine ⟨
    by unfold trinary_hardware_live_observable_count; norm_num,
    by unfold trinary_hardware_live_D_eff; norm_num,
    trinary_hardware_live_median_error_under_five_pct,
    ai_raw_S_positive
  ⟩

end

end FSOT.Formal
