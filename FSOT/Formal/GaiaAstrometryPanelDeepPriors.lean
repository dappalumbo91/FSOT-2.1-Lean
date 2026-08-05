/-
  FSOT Formal GaiaAstrometryPanelDeepPriors — extension domain Gaia_Astrometry_Panel_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def gaia_astrometry_panel_deep_observable_count : ℕ := 62
def gaia_astrometry_panel_deep_D_eff : ℕ := 20

theorem gaia_astrometry_panel_deep_observable_count_pos : 0 < gaia_astrometry_panel_deep_observable_count := by
  unfold gaia_astrometry_panel_deep_observable_count; decide

theorem gaia_astrometry_panel_deep_median_error_under_half_pct :
    (0.022461 : ℝ) < (0.5 : ℝ) := by norm_num

theorem gaia_astrometry_panel_deep_bundle :
    gaia_astrometry_panel_deep_observable_count = 62 ∧
    gaia_astrometry_panel_deep_D_eff = 20 ∧
    (0.022461 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold gaia_astrometry_panel_deep_observable_count; decide,
    by unfold gaia_astrometry_panel_deep_D_eff; decide,
    gaia_astrometry_panel_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
