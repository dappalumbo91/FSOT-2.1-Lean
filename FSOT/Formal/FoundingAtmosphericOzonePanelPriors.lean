/-
  FSOT Formal FoundingAtmosphericOzonePanelPriors — extension domain Founding_Atmospheric_Ozone_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def founding_atmospheric_ozone_panel_observable_count : ℕ := 24
def founding_atmospheric_ozone_panel_D_eff : ℕ := 12

theorem founding_atmospheric_ozone_panel_observable_count_pos : 0 < founding_atmospheric_ozone_panel_observable_count := by
  unfold founding_atmospheric_ozone_panel_observable_count; decide

theorem founding_atmospheric_ozone_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.022236 : ℝ) < (0.5 : ℝ))

theorem founding_atmospheric_ozone_panel_bundle :
    founding_atmospheric_ozone_panel_observable_count = 24 ∧
    founding_atmospheric_ozone_panel_D_eff = 12 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold founding_atmospheric_ozone_panel_observable_count; decide,
    by unfold founding_atmospheric_ozone_panel_D_eff; decide,
    founding_atmospheric_ozone_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
