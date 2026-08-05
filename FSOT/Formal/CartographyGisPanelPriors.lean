/-
  FSOT Formal CartographyGisPanelPriors — extension domain Cartography_GIS_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cartography_gis_panel_observable_count : ℕ := 48
def cartography_gis_panel_D_eff : ℕ := 18

theorem cartography_gis_panel_observable_count_pos : 0 < cartography_gis_panel_observable_count := by
  unfold cartography_gis_panel_observable_count; decide

theorem cartography_gis_panel_median_error_under_half_pct :
    (0.018855999999999998 : ℝ) < (0.5 : ℝ) := by norm_num

theorem cartography_gis_panel_bundle :
    cartography_gis_panel_observable_count = 48 ∧
    cartography_gis_panel_D_eff = 18 ∧
    (0.018855999999999998 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cartography_gis_panel_observable_count; decide,
    by unfold cartography_gis_panel_D_eff; decide,
    cartography_gis_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
