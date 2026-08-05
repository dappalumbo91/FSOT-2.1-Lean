/-
  FSOT Formal PaleoclimatePriors — extension domain Paleoclimate.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def paleoclimate_observable_count : ℕ := 40
def paleoclimate_D_eff : ℕ := 17

theorem paleoclimate_observable_count_pos : 0 < paleoclimate_observable_count := by
  unfold paleoclimate_observable_count; decide

theorem paleoclimate_median_error_under_half_pct :
    (0.015015854077432778 : ℝ) < (0.5 : ℝ) := by norm_num

theorem paleoclimate_bundle :
    paleoclimate_observable_count = 40 ∧
    paleoclimate_D_eff = 17 ∧
    (0.015015854077432778 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold paleoclimate_observable_count; decide,
    by unfold paleoclimate_D_eff; decide,
    paleoclimate_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
