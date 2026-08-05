/-
  FSOT Formal SoilSciencePriors — Tier 82 scientific expansion (Soil_Science_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def soil_science_observable_count : ℕ := 96
def soil_science_median_error_pct : ℝ := (0.006006 : ℝ)
def soil_science_D_eff : ℕ := 15

theorem soil_science_observable_count_pos : 0 < soil_science_observable_count := by
  unfold soil_science_observable_count; decide

theorem soil_science_median_error_under_five_pct :
    soil_science_median_error_pct < (5 : ℝ) := by
  unfold soil_science_median_error_pct; norm_num

theorem soil_science_bundle :
    soil_science_observable_count = 96 ∧
    soil_science_D_eff = 15 ∧
    soil_science_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold soil_science_observable_count; decide,
    by unfold soil_science_D_eff; decide,
    soil_science_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
