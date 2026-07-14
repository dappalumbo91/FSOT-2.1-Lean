/-
  FSOT Formal QuantumMaterialsPriors — condensed-matter SMILES observables.
  Generator: scripts/gen_quantum_materials_lean.py
  Source: vendor/smiles
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_materials_observable_count : ℕ := 168
def quantum_materials_section_count : ℕ := 13
def quantum_materials_D_eff : ℕ := 16
def quantum_materials_pooled_median_error_pct : ℝ := (0.024318115591995593 : ℝ)
def quantum_materials_headline_median_error_pct : ℝ := (0.01692529386942307 : ℝ)
def quantum_materials_beats_sota_headlines : ℕ := 6

theorem quantum_materials_observable_count_pos : 0 < quantum_materials_observable_count := by
  unfold quantum_materials_observable_count; norm_num

theorem quantum_materials_section_count_pos : 0 < quantum_materials_section_count := by
  unfold quantum_materials_section_count; norm_num

theorem quantum_materials_pooled_median_under_half_pct :
    quantum_materials_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_materials_pooled_median_error_pct; norm_num

theorem quantum_materials_headline_median_under_half_pct :
    quantum_materials_headline_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_materials_headline_median_error_pct; norm_num

theorem quantum_materials_beats_sota_headlines_pos : 0 < quantum_materials_beats_sota_headlines := by
  unfold quantum_materials_beats_sota_headlines; norm_num

/-- Bundle: Quantum Materials condensed-matter SMILES depth with material/quantum maps. -/
theorem quantum_materials_bundle :
    quantum_materials_observable_count = 168 ∧
    quantum_materials_section_count = 13 ∧
    quantum_materials_D_eff = 16 ∧
    quantum_materials_pooled_median_error_pct < (0.5 : ℝ) ∧
    quantum_materials_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < quantum_materials_beats_sota_headlines ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold quantum_materials_observable_count; norm_num,
    by unfold quantum_materials_section_count; norm_num,
    by unfold quantum_materials_D_eff; norm_num,
    quantum_materials_pooled_median_under_half_pct,
    quantum_materials_headline_median_under_half_pct,
    quantum_materials_beats_sota_headlines_pos,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
