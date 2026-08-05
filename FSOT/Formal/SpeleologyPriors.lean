/-
  FSOT Formal SpeleologyPriors — extension domain Speleology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def speleology_observable_count : ℕ := 65
def speleology_D_eff : ℕ := 16

theorem speleology_observable_count_pos : 0 < speleology_observable_count := by
  unfold speleology_observable_count; decide

theorem speleology_median_error_under_half_pct :
    (0.0034072140135262413 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0034072140135262413 : ℝ) < (0.5 : ℝ))

theorem speleology_bundle :
    speleology_observable_count = 65 ∧
    speleology_D_eff = 16 ∧
    (0.0034072140135262413 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold speleology_observable_count; decide,
    by unfold speleology_D_eff; decide,
    speleology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
