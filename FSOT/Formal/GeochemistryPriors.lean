/-
  FSOT Formal GeochemistryPriors — SMILES mineral/geo + planetary bulk density.
  Generator: scripts/gen_geochemistry_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def geochemistry_observable_count : ℕ := 153
def geochemistry_median_error_pct : ℝ := (0.006625234573930708 : ℝ)
def geochemistry_D_eff : ℕ := 15

theorem geochemistry_observable_count_pos : 0 < geochemistry_observable_count := by
  unfold geochemistry_observable_count; decide

theorem geochemistry_median_error_under_half_pct :
    geochemistry_median_error_pct < (0.5 : ℝ) := by
  unfold geochemistry_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem geochemistry_bundle :
    geochemistry_observable_count = 153 ∧
    geochemistry_D_eff = 15 ∧
    geochemistry_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold geochemistry_observable_count; decide,
    by unfold geochemistry_D_eff; decide,
    geochemistry_median_error_under_half_pct,
    galactic_raw_S_positive
  ⟩

end

end FSOT.Formal
