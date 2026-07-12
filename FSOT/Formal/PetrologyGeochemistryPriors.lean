/-
  FSOT Formal PetrologyGeochemistryPriors — Tier 82 scientific expansion (Petrology_Geochemistry_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def petrology_observable_count : ℕ := 80
def petrology_median_error_pct : ℝ := (0.030428 : ℝ)
def petrology_D_eff : ℕ := 14

theorem petrology_observable_count_pos : 0 < petrology_observable_count := by
  unfold petrology_observable_count; norm_num

theorem petrology_median_error_under_five_pct :
    petrology_median_error_pct < (5 : ℝ) := by
  unfold petrology_median_error_pct; norm_num

theorem petrology_bundle :
    petrology_observable_count = 80 ∧
    petrology_D_eff = 14 ∧
    petrology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold petrology_observable_count; norm_num,
    by unfold petrology_D_eff; norm_num,
    petrology_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
