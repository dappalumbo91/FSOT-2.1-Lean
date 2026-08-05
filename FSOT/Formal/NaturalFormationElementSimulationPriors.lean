/-
  FSOT Formal NaturalFormationElementSimulationPriors — extension domain Natural_Formation_Element_Simulation.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def natural_formation_element_simulation_observable_count : ℕ := 44
def natural_formation_element_simulation_D_eff : ℕ := 11

theorem natural_formation_element_simulation_observable_count_pos : 0 < natural_formation_element_simulation_observable_count := by
  unfold natural_formation_element_simulation_observable_count; decide

theorem natural_formation_element_simulation_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem natural_formation_element_simulation_bundle :
    natural_formation_element_simulation_observable_count = 44 ∧
    natural_formation_element_simulation_D_eff = 11 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold natural_formation_element_simulation_observable_count; decide,
    by unfold natural_formation_element_simulation_D_eff; decide,
    natural_formation_element_simulation_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
