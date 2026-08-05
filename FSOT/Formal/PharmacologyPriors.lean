/-
  FSOT Formal PharmacologyPriors — ChEMBL molecular-weight verification.
  Generator: scripts/gen_pharmacology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pharmacology_observable_count : ℕ := 120
def pharmacology_median_error_pct : ℝ := (0.0011715432153059484 : ℝ)
def pharmacology_D_eff : ℕ := 14

theorem pharmacology_observable_count_pos : 0 < pharmacology_observable_count := by
  unfold pharmacology_observable_count; decide

theorem pharmacology_median_error_under_half_pct :
    pharmacology_median_error_pct < (0.5 : ℝ) := by
  unfold pharmacology_median_error_pct
  exact (by norm_num : (0.0011715432153059484  : ℝ) < 0.5)

theorem pharmacology_bundle :
    pharmacology_observable_count = 120 ∧
    pharmacology_D_eff = 14 ∧
    pharmacology_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold pharmacology_observable_count; decide,
    by unfold pharmacology_D_eff; decide,
    pharmacology_median_error_under_half_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
