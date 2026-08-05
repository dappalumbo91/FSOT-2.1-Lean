/-
  FSOT Formal RadioAstronomyPriors — Tier 82 scientific expansion (Radio_Astronomy_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def radio_astronomy_observable_count : ℕ := 30
def radio_astronomy_median_error_pct : ℝ := (0.022461 : ℝ)
def radio_astronomy_D_eff : ℕ := 20

theorem radio_astronomy_observable_count_pos : 0 < radio_astronomy_observable_count := by
  unfold radio_astronomy_observable_count; decide

theorem radio_astronomy_median_error_under_five_pct :
    radio_astronomy_median_error_pct < (5 : ℝ) := by
  unfold radio_astronomy_median_error_pct
  exact (by norm_num : (0.022461  : ℝ) < (5 : ℝ))

theorem radio_astronomy_bundle :
    radio_astronomy_observable_count = 30 ∧
    radio_astronomy_D_eff = 20 ∧
    radio_astronomy_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold radio_astronomy_observable_count; decide,
    by unfold radio_astronomy_D_eff; decide,
    radio_astronomy_median_error_under_five_pct,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
