/-
  FSOT Formal ToxicologyPriors — Tier 82 scientific expansion (Toxicology_Panel).
  Generator: scripts/gen_tier82_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def toxicology_observable_count : ℕ := 21
def toxicology_median_error_pct : ℝ := (0.033401 : ℝ)
def toxicology_D_eff : ℕ := 13

theorem toxicology_observable_count_pos : 0 < toxicology_observable_count := by
  unfold toxicology_observable_count; norm_num

theorem toxicology_median_error_under_five_pct :
    toxicology_median_error_pct < (5 : ℝ) := by
  unfold toxicology_median_error_pct; norm_num

theorem toxicology_bundle :
    toxicology_observable_count = 21 ∧
    toxicology_D_eff = 13 ∧
    toxicology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold toxicology_observable_count; norm_num,
    by unfold toxicology_D_eff; norm_num,
    toxicology_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
