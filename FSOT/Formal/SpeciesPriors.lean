/-
  FSOT Formal SpeciesPriors — Machine & Molecule catalog certificates.

  Source: FSOT_Machine_And_Molecule/fsot_species_catalog.json
  Generator: scripts/gen_species_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def species_metal_count : ℕ := 44
def species_molecule_count : ℕ := 87
def species_polymer_count : ℕ := 10
def species_total_count : ℕ := 141
def species_property_count : ℕ := 684

theorem species_total_count_eq_sum :
    species_metal_count + species_molecule_count + species_polymer_count = species_total_count := by
  unfold species_metal_count species_molecule_count species_polymer_count species_total_count; norm_num

theorem species_property_count_pos : 0 < species_property_count := by
  unfold species_property_count; norm_num

/-- Bundle: 141 species across metals/molecules/polymers; material+molecular domain signs. -/
theorem species_catalog_bundle :
    species_total_count = 141 ∧
    species_metal_count = 44 ∧
    species_molecule_count = 87 ∧
    species_polymer_count = 10 ∧
    species_metal_count + species_molecule_count + species_polymer_count = species_total_count ∧
    species_property_count = 684 ∧
    (0 : ℝ) < raw_S (get_domain_params "material") ∧
    (0 : ℝ) < raw_S (get_domain_params "molecular") := by
  refine ⟨
    by unfold species_total_count; norm_num,
    by unfold species_metal_count; norm_num,
    by unfold species_molecule_count; norm_num,
    by unfold species_polymer_count; norm_num,
    species_total_count_eq_sum,
    by unfold species_property_count; norm_num,
    material_raw_S_positive,
    molecular_raw_S_positive
  ⟩

end

end FSOT.Formal
