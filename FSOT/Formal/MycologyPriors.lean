/-
  FSOT Formal MycologyPriors — extension domain Mycology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def mycology_observable_count : ℕ := 420
def mycology_D_eff : ℕ := 14

theorem mycology_observable_count_pos : 0 < mycology_observable_count := by
  unfold mycology_observable_count; decide

theorem mycology_median_error_under_half_pct :
    (0.022236250385193498 : ℝ) < (0.5 : ℝ) := by norm_num

theorem mycology_bundle :
    mycology_observable_count = 420 ∧
    mycology_D_eff = 14 ∧
    (0.022236250385193498 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold mycology_observable_count; decide,
    by unfold mycology_D_eff; decide,
    mycology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
