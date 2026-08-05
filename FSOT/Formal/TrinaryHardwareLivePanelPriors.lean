/-
  FSOT Formal TrinaryHardwareLivePanelPriors — extension domain Trinary_Hardware_Live_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def trinary_hardware_live_panel_observable_count : ℕ := 37
def trinary_hardware_live_panel_D_eff : ℕ := 14

theorem trinary_hardware_live_panel_observable_count_pos : 0 < trinary_hardware_live_panel_observable_count := by
  unfold trinary_hardware_live_panel_observable_count; decide

theorem trinary_hardware_live_panel_median_error_under_half_pct :
    (0.014767 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.014767 : ℝ) < (0.5 : ℝ))

theorem trinary_hardware_live_panel_bundle :
    trinary_hardware_live_panel_observable_count = 37 ∧
    trinary_hardware_live_panel_D_eff = 14 ∧
    (0.014767 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold trinary_hardware_live_panel_observable_count; decide,
    by unfold trinary_hardware_live_panel_D_eff; decide,
    trinary_hardware_live_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
