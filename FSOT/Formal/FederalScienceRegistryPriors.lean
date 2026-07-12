/-
  FSOT Formal FederalScienceRegistryPriors — Tier 80 government open data (Federal_Science_Registry_Panel).
  Generator: scripts/gen_tier80_government_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def federal_science_registry_observable_count : ℕ := 16
def federal_science_registry_median_error_pct : ℝ := (0.024225 : ℝ)
def federal_science_registry_D_eff : ℕ := 17

theorem federal_science_registry_observable_count_pos : 0 < federal_science_registry_observable_count := by
  unfold federal_science_registry_observable_count; norm_num

theorem federal_science_registry_median_error_under_five_pct :
    federal_science_registry_median_error_pct < (5 : ℝ) := by
  unfold federal_science_registry_median_error_pct; norm_num

theorem federal_science_registry_bundle :
    federal_science_registry_observable_count = 16 ∧
    federal_science_registry_D_eff = 17 ∧
    federal_science_registry_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold federal_science_registry_observable_count; norm_num,
    by unfold federal_science_registry_D_eff; norm_num,
    federal_science_registry_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
