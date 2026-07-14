/-
  FSOT Formal MaterialsSpeciesBridgePriors — SMILES engineering ↔ species catalog metals.
  Generator: scripts/gen_materials_species_bridge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def materials_species_bridge_observable_count : ℕ := 45
def materials_species_bridge_median_error_pct : ℝ := (0.0 : ℝ)
def materials_species_bridge_D_eff : ℕ := 14

theorem materials_species_bridge_observable_count_pos : 0 < materials_species_bridge_observable_count := by
  unfold materials_species_bridge_observable_count; norm_num

theorem materials_species_bridge_median_error_under_five_pct :
    materials_species_bridge_median_error_pct < (5 : ℝ) := by
  unfold materials_species_bridge_median_error_pct; norm_num

theorem materials_species_bridge_bundle :
    materials_species_bridge_observable_count = 45 ∧
    materials_species_bridge_D_eff = 14 ∧
    materials_species_bridge_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold materials_species_bridge_observable_count; norm_num,
    by unfold materials_species_bridge_D_eff; norm_num,
    materials_species_bridge_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
