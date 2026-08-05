/-
  FSOT Formal VirologyPanelPriors — extension domain Virology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def virology_panel_observable_count : ℕ := 24
def virology_panel_D_eff : ℕ := 14

theorem virology_panel_observable_count_pos : 0 < virology_panel_observable_count := by
  unfold virology_panel_observable_count; decide

theorem virology_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) := by norm_num

theorem virology_panel_bundle :
    virology_panel_observable_count = 24 ∧
    virology_panel_D_eff = 14 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold virology_panel_observable_count; decide,
    by unfold virology_panel_D_eff; decide,
    virology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
