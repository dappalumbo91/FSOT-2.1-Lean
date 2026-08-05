/-
  FSOT Formal VolcanologyPriors — Tier 82 scientific expansion (Volcanology_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def volcanology_observable_count : ℕ := 90
def volcanology_median_error_pct : ℝ := (0.023502 : ℝ)
def volcanology_D_eff : ℕ := 19

theorem volcanology_observable_count_pos : 0 < volcanology_observable_count := by
  unfold volcanology_observable_count; decide

theorem volcanology_median_error_under_five_pct :
    volcanology_median_error_pct < (5 : ℝ) := by
  unfold volcanology_median_error_pct; norm_num

theorem volcanology_bundle :
    volcanology_observable_count = 90 ∧
    volcanology_D_eff = 19 ∧
    volcanology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold volcanology_observable_count; decide,
    by unfold volcanology_D_eff; decide,
    volcanology_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
