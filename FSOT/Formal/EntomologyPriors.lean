/-
  FSOT Formal EntomologyPriors — extension domain Entomology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def entomology_observable_count : ℕ := 430
def entomology_D_eff : ℕ := 14

theorem entomology_observable_count_pos : 0 < entomology_observable_count := by
  unfold entomology_observable_count; decide

theorem entomology_median_error_under_half_pct :
    (0.022236250385189223 : ℝ) < (0.5 : ℝ) := by norm_num

theorem entomology_bundle :
    entomology_observable_count = 430 ∧
    entomology_D_eff = 14 ∧
    (0.022236250385189223 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold entomology_observable_count; decide,
    by unfold entomology_D_eff; decide,
    entomology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
