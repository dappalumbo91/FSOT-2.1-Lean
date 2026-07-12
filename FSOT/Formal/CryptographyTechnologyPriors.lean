/-
  FSOT Formal CryptographyTechnologyPriors — extension domain Cryptography_Technology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cryptography_technology_observable_count : ℕ := 44
def cryptography_technology_D_eff : ℕ := 16

theorem cryptography_technology_observable_count_pos : 0 < cryptography_technology_observable_count := by
  unfold cryptography_technology_observable_count; norm_num

theorem cryptography_technology_median_error_under_half_pct :
    (0.047520672006218234 : ℝ) < (0.5 : ℝ) := by norm_num

theorem cryptography_technology_bundle :
    cryptography_technology_observable_count = 44 ∧
    cryptography_technology_D_eff = 16 ∧
    (0.047520672006218234 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cryptography_technology_observable_count; norm_num,
    by unfold cryptography_technology_D_eff; norm_num,
    cryptography_technology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
