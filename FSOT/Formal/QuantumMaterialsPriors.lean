/-
  FSOT Formal QuantumMaterialsPriors — condensed-matter SMILES observables.
  Generator: scripts/gen_quantum_materials_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_materials_observable_count : ℕ := 168
def quantum_materials_median_error_pct : ℝ := (0.857198 : ℝ)
def quantum_materials_D_eff : ℕ := 16

theorem quantum_materials_observable_count_pos : 0 < quantum_materials_observable_count := by
  unfold quantum_materials_observable_count; norm_num

theorem quantum_materials_median_error_under_five_pct :
    quantum_materials_median_error_pct < (5 : ℝ) := by
  unfold quantum_materials_median_error_pct; norm_num

theorem quantum_materials_bundle :
    quantum_materials_observable_count = 168 ∧
    quantum_materials_D_eff = 16 ∧
    quantum_materials_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold quantum_materials_observable_count; norm_num,
    by unfold quantum_materials_D_eff; norm_num,
    quantum_materials_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
