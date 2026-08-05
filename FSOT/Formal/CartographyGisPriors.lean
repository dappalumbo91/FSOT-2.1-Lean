/-
  FSOT Formal CartographyGisPriors — Tier 82 scientific expansion (Cartography_GIS_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def cartography_gis_observable_count : ℕ := 48
def cartography_gis_median_error_pct : ℝ := (0.018855999999999998 : ℝ)
def cartography_gis_D_eff : ℕ := 18

theorem cartography_gis_observable_count_pos : 0 < cartography_gis_observable_count := by
  unfold cartography_gis_observable_count; decide

theorem cartography_gis_median_error_under_five_pct :
    cartography_gis_median_error_pct < (5 : ℝ) := by
  unfold cartography_gis_median_error_pct
  exact (by norm_num : (0.018855999999999998  : ℝ) < (5 : ℝ))

theorem cartography_gis_bundle :
    cartography_gis_observable_count = 48 ∧
    cartography_gis_D_eff = 18 ∧
    cartography_gis_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "economic") > 0 := by
  refine ⟨
    by unfold cartography_gis_observable_count; decide,
    by unfold cartography_gis_D_eff; decide,
    cartography_gis_median_error_under_five_pct,
    economic_raw_S_positive
  ⟩

end

end FSOT.Formal
