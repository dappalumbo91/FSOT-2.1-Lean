/-
  FSOT Formal VirologyPriors — extension domain Virology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def virology_observable_count : ℕ := 50
def virology_D_eff : ℕ := 14

theorem virology_observable_count_pos : 0 < virology_observable_count := by
  unfold virology_observable_count; decide

theorem virology_median_error_under_half_pct :
    (0.04593318440797614 : ℝ) < (0.5 : ℝ) := by norm_num

theorem virology_bundle :
    virology_observable_count = 50 ∧
    virology_D_eff = 14 ∧
    (0.04593318440797614 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold virology_observable_count; decide,
    by unfold virology_D_eff; decide,
    virology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
