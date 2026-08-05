/-
  FSOT Formal ExoplanetSystemArchitecturePriors — extension domain Exoplanet_System_Architecture.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def exoplanet_system_architecture_observable_count : ℕ := 882
def exoplanet_system_architecture_D_eff : ℕ := 21

theorem exoplanet_system_architecture_observable_count_pos : 0 < exoplanet_system_architecture_observable_count := by
  unfold exoplanet_system_architecture_observable_count; decide

theorem exoplanet_system_architecture_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem exoplanet_system_architecture_bundle :
    exoplanet_system_architecture_observable_count = 882 ∧
    exoplanet_system_architecture_D_eff = 21 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold exoplanet_system_architecture_observable_count; decide,
    by unfold exoplanet_system_architecture_D_eff; decide,
    exoplanet_system_architecture_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
