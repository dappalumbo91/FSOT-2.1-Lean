/-
  FSOT Formal LongevityAnAgeCatalogPanelPriors — Tier 94 longevity genetics (Longevity_AnAge_Catalog_Panel).
  Generator: scripts/gen_tier94_longevity_genetics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def longevity_anage_catalog_observable_count : ℕ := 966
def longevity_anage_catalog_median_error_pct : ℝ := (0.022236 : ℝ)
def longevity_anage_catalog_D_eff : ℕ := 20

theorem longevity_anage_catalog_observable_count_pos : 0 < longevity_anage_catalog_observable_count := by
  unfold longevity_anage_catalog_observable_count; decide

theorem longevity_anage_catalog_median_error_under_five_pct :
    longevity_anage_catalog_median_error_pct < (5 : ℝ) := by
  unfold longevity_anage_catalog_median_error_pct; norm_num

theorem longevity_anage_catalog_bundle :
    longevity_anage_catalog_observable_count = 966 ∧
    longevity_anage_catalog_D_eff = 20 ∧
    longevity_anage_catalog_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold longevity_anage_catalog_observable_count; decide,
    by unfold longevity_anage_catalog_D_eff; decide,
    longevity_anage_catalog_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
