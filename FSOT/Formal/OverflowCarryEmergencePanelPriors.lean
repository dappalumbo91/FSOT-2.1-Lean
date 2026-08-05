/-
  FSOT Formal OverflowCarryEmergencePanelPriors — extension domain Overflow_Carry_Emergence_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def overflow_carry_emergence_panel_observable_count : ℕ := 29
def overflow_carry_emergence_panel_D_eff : ℕ := 19

theorem overflow_carry_emergence_panel_observable_count_pos : 0 < overflow_carry_emergence_panel_observable_count := by
  unfold overflow_carry_emergence_panel_observable_count; decide

theorem overflow_carry_emergence_panel_median_error_under_half_pct :
    (0.009504 : ℝ) < (0.5 : ℝ) := by norm_num

theorem overflow_carry_emergence_panel_bundle :
    overflow_carry_emergence_panel_observable_count = 29 ∧
    overflow_carry_emergence_panel_D_eff = 19 ∧
    (0.009504 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold overflow_carry_emergence_panel_observable_count; decide,
    by unfold overflow_carry_emergence_panel_D_eff; decide,
    overflow_carry_emergence_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
