/-
  FSOT Formal LimnologyPriors — Tier 82 scientific expansion (Limnology_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def limnology_observable_count : ℕ := 2010
def limnology_median_error_pct : ℝ := (0.030173 : ℝ)
def limnology_D_eff : ℕ := 16

theorem limnology_observable_count_pos : 0 < limnology_observable_count := by
  unfold limnology_observable_count; decide

theorem limnology_median_error_under_five_pct :
    limnology_median_error_pct < (5 : ℝ) := by
  unfold limnology_median_error_pct
  exact (by norm_num : (0.030173  : ℝ) < (5 : ℝ))

theorem limnology_bundle :
    limnology_observable_count = 2010 ∧
    limnology_D_eff = 16 ∧
    limnology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold limnology_observable_count; decide,
    by unfold limnology_D_eff; decide,
    limnology_median_error_under_five_pct,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
