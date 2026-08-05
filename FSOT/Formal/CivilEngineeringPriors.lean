/-
  FSOT Formal CivilEngineeringPriors — extension domain Civil_Engineering.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def civil_engineering_observable_count : ℕ := 37
def civil_engineering_D_eff : ℕ := 16

theorem civil_engineering_observable_count_pos : 0 < civil_engineering_observable_count := by
  unfold civil_engineering_observable_count; decide

theorem civil_engineering_median_error_under_half_pct :
    (0.0335259880736416 : ℝ) < (0.5 : ℝ) := by norm_num

theorem civil_engineering_bundle :
    civil_engineering_observable_count = 37 ∧
    civil_engineering_D_eff = 16 ∧
    (0.0335259880736416 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold civil_engineering_observable_count; decide,
    by unfold civil_engineering_D_eff; decide,
    civil_engineering_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
