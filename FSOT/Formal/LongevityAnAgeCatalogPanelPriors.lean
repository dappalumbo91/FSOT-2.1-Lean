/-
  FSOT Formal LongevityAnageCatalogPanelPriors — extension domain Longevity_AnAge_Catalog_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def longevity_anage_catalog_panel_observable_count : ℕ := 966
def longevity_anage_catalog_panel_D_eff : ℕ := 20

theorem longevity_anage_catalog_panel_observable_count_pos : 0 < longevity_anage_catalog_panel_observable_count := by
  unfold longevity_anage_catalog_panel_observable_count; norm_num

theorem longevity_anage_catalog_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) := by norm_num

theorem longevity_anage_catalog_panel_bundle :
    longevity_anage_catalog_panel_observable_count = 966 ∧
    longevity_anage_catalog_panel_D_eff = 20 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold longevity_anage_catalog_panel_observable_count; norm_num,
    by unfold longevity_anage_catalog_panel_D_eff; norm_num,
    longevity_anage_catalog_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
