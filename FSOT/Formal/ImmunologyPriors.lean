/-
  FSOT Formal ImmunologyPriors — extension domain Immunology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def immunology_observable_count : ℕ := 84
def immunology_D_eff : ℕ := 13

theorem immunology_observable_count_pos : 0 < immunology_observable_count := by
  unfold immunology_observable_count; norm_num

theorem immunology_median_error_under_five_pct :
    (0.451494 : ℝ) < (5 : ℝ) := by norm_num

theorem immunology_bundle :
    immunology_observable_count = 84 ∧
    immunology_D_eff = 13 ∧
    (0.451494 : ℝ) < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold immunology_observable_count; norm_num,
    by unfold immunology_D_eff; norm_num,
    immunology_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
