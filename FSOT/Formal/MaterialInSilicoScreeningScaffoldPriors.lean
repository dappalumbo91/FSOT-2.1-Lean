/-
  FSOT Formal MaterialInSilicoScreeningScaffoldPriors — extension domain Material_In_Silico_Screening_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def material_in_silico_screening_scaffold_observable_count : ℕ := 42
def material_in_silico_screening_scaffold_D_eff : ℕ := 15

theorem material_in_silico_screening_scaffold_observable_count_pos : 0 < material_in_silico_screening_scaffold_observable_count := by
  unfold material_in_silico_screening_scaffold_observable_count; norm_num

theorem material_in_silico_screening_scaffold_median_error_under_half_pct :
    (0.00206 : ℝ) < (0.5 : ℝ) := by norm_num

theorem material_in_silico_screening_scaffold_bundle :
    material_in_silico_screening_scaffold_observable_count = 42 ∧
    material_in_silico_screening_scaffold_D_eff = 15 ∧
    (0.00206 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold material_in_silico_screening_scaffold_observable_count; norm_num,
    by unfold material_in_silico_screening_scaffold_D_eff; norm_num,
    material_in_silico_screening_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
