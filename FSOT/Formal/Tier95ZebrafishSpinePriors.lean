/-
  FSOT Formal Tier95ZebrafishSpinePriors — Tier 95 Zebrahub developmental (Tier_95_Zebrafish_Spine).
  Generator: scripts/gen_tier95_zebrahub_development_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def tier_95_zebrafish_observable_count : ℕ := 18
def tier_95_zebrafish_median_error_pct : ℝ := (0.0 : ℝ)
def tier_95_zebrafish_D_eff : ℕ := 23

theorem tier_95_zebrafish_observable_count_pos : 0 < tier_95_zebrafish_observable_count := by
  unfold tier_95_zebrafish_observable_count; decide

theorem tier_95_zebrafish_median_error_under_five_pct :
    tier_95_zebrafish_median_error_pct < (5 : ℝ) := by
  unfold tier_95_zebrafish_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem tier_95_zebrafish_bundle :
    tier_95_zebrafish_observable_count = 18 ∧
    tier_95_zebrafish_D_eff = 23 ∧
    tier_95_zebrafish_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold tier_95_zebrafish_observable_count; decide,
    by unfold tier_95_zebrafish_D_eff; decide,
    tier_95_zebrafish_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
