/-
  FSOT Formal EthologyPriors — Tier 82 scientific expansion (Ethology_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def ethology_observable_count : ℕ := 100
def ethology_median_error_pct : ℝ := (0.006607 : ℝ)
def ethology_D_eff : ℕ := 15

theorem ethology_observable_count_pos : 0 < ethology_observable_count := by
  unfold ethology_observable_count; decide

theorem ethology_median_error_under_five_pct :
    ethology_median_error_pct < (5 : ℝ) := by
  unfold ethology_median_error_pct
  exact (by norm_num : (0.006607  : ℝ) < (5 : ℝ))

theorem ethology_bundle :
    ethology_observable_count = 100 ∧
    ethology_D_eff = 15 ∧
    ethology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold ethology_observable_count; decide,
    by unfold ethology_D_eff; decide,
    ethology_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
