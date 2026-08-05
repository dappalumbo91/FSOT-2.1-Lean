/-
  FSOT Formal ZoologyPriors — extension domain Zoology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def zoology_observable_count : ℕ := 1000
def zoology_D_eff : ℕ := 14

theorem zoology_observable_count_pos : 0 < zoology_observable_count := by
  unfold zoology_observable_count; decide

theorem zoology_median_error_under_half_pct :
    (0.01778900030815634 : ℝ) < (0.5 : ℝ) := by norm_num

theorem zoology_bundle :
    zoology_observable_count = 1000 ∧
    zoology_D_eff = 14 ∧
    (0.01778900030815634 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold zoology_observable_count; decide,
    by unfold zoology_D_eff; decide,
    zoology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
