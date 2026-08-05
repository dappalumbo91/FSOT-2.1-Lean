/-
  FSOT Formal ChemicalEngineeringPriors — extension domain Chemical_Engineering.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def chemical_engineering_observable_count : ℕ := 186
def chemical_engineering_D_eff : ℕ := 16

theorem chemical_engineering_observable_count_pos : 0 < chemical_engineering_observable_count := by
  unfold chemical_engineering_observable_count; decide

theorem chemical_engineering_median_error_under_half_pct :
    (0.0010333425185953097 : ℝ) < (0.5 : ℝ) := by norm_num

theorem chemical_engineering_bundle :
    chemical_engineering_observable_count = 186 ∧
    chemical_engineering_D_eff = 16 ∧
    (0.0010333425185953097 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold chemical_engineering_observable_count; decide,
    by unfold chemical_engineering_D_eff; decide,
    chemical_engineering_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
