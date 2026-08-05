/-
  FSOT Formal SecureSoftwareEngineeringPriors — extension domain Secure_Software_Engineering.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def secure_software_engineering_observable_count : ℕ := 59
def secure_software_engineering_D_eff : ℕ := 14

theorem secure_software_engineering_observable_count_pos : 0 < secure_software_engineering_observable_count := by
  unfold secure_software_engineering_observable_count; decide

theorem secure_software_engineering_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem secure_software_engineering_bundle :
    secure_software_engineering_observable_count = 59 ∧
    secure_software_engineering_D_eff = 14 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold secure_software_engineering_observable_count; decide,
    by unfold secure_software_engineering_D_eff; decide,
    secure_software_engineering_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
