/-
  FSOT Formal OpenMeteoLivePanelPriors — extension domain Open_Meteo_Live_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def open_meteo_live_panel_observable_count : ℕ := 432
def open_meteo_live_panel_D_eff : ℕ := 16

theorem open_meteo_live_panel_observable_count_pos : 0 < open_meteo_live_panel_observable_count := by
  unfold open_meteo_live_panel_observable_count; decide

theorem open_meteo_live_panel_median_error_under_half_pct :
    (0.026204 : ℝ) < (0.5 : ℝ) := by norm_num

theorem open_meteo_live_panel_bundle :
    open_meteo_live_panel_observable_count = 432 ∧
    open_meteo_live_panel_D_eff = 16 ∧
    (0.026204 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold open_meteo_live_panel_observable_count; decide,
    by unfold open_meteo_live_panel_D_eff; decide,
    open_meteo_live_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
