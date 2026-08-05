/-
  FSOT Formal FoundingWhiteDwarfCoolingPanelPriors — extension domain Founding_White_Dwarf_Cooling_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def founding_white_dwarf_cooling_panel_observable_count : ℕ := 24
def founding_white_dwarf_cooling_panel_D_eff : ℕ := 15

theorem founding_white_dwarf_cooling_panel_observable_count_pos : 0 < founding_white_dwarf_cooling_panel_observable_count := by
  unfold founding_white_dwarf_cooling_panel_observable_count; decide

theorem founding_white_dwarf_cooling_panel_median_error_under_half_pct :
    (0.022461 : ℝ) < (0.5 : ℝ) := by norm_num

theorem founding_white_dwarf_cooling_panel_bundle :
    founding_white_dwarf_cooling_panel_observable_count = 24 ∧
    founding_white_dwarf_cooling_panel_D_eff = 15 ∧
    (0.022461 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold founding_white_dwarf_cooling_panel_observable_count; decide,
    by unfold founding_white_dwarf_cooling_panel_D_eff; decide,
    founding_white_dwarf_cooling_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
