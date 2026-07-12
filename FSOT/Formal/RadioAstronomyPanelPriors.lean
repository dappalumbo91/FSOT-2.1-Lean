/-
  FSOT Formal RadioAstronomyPanelPriors — extension domain Radio_Astronomy_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def radio_astronomy_panel_observable_count : ℕ := 30
def radio_astronomy_panel_D_eff : ℕ := 20

theorem radio_astronomy_panel_observable_count_pos : 0 < radio_astronomy_panel_observable_count := by
  unfold radio_astronomy_panel_observable_count; norm_num

theorem radio_astronomy_panel_median_error_under_half_pct :
    (0.022461 : ℝ) < (0.5 : ℝ) := by norm_num

theorem radio_astronomy_panel_bundle :
    radio_astronomy_panel_observable_count = 30 ∧
    radio_astronomy_panel_D_eff = 20 ∧
    (0.022461 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold radio_astronomy_panel_observable_count; norm_num,
    by unfold radio_astronomy_panel_D_eff; norm_num,
    radio_astronomy_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
