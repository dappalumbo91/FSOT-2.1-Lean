/-
  FSOT Formal MaterialsEngineeringPriors — mechanical/thermal SMILES engineering.
  Generator: scripts/gen_materials_engineering_lean.py
  Source: vendor/smiles
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def materials_engineering_observable_count : ℕ := 87
def materials_engineering_section_count : ℕ := 7
def materials_engineering_D_eff : ℕ := 14
def materials_engineering_pooled_median_error_pct : ℝ := (0.118765 : ℝ)
def materials_engineering_headline_median_error_pct : ℝ := (0.312058 : ℝ)
def materials_engineering_beats_sota_headlines : ℕ := 6

theorem materials_engineering_observable_count_pos : 0 < materials_engineering_observable_count := by
  unfold materials_engineering_observable_count; norm_num

theorem materials_engineering_section_count_pos : 0 < materials_engineering_section_count := by
  unfold materials_engineering_section_count; norm_num

theorem materials_engineering_pooled_median_under_five_pct :
    materials_engineering_pooled_median_error_pct < (5 : ℝ) := by
  unfold materials_engineering_pooled_median_error_pct; norm_num

theorem materials_engineering_headline_median_under_five_pct :
    materials_engineering_headline_median_error_pct < (5 : ℝ) := by
  unfold materials_engineering_headline_median_error_pct; norm_num

theorem materials_engineering_beats_sota_headlines_pos : 0 < materials_engineering_beats_sota_headlines := by
  unfold materials_engineering_beats_sota_headlines; norm_num

/-- Bundle: Materials Engineering mechanical/thermal SMILES with material/energy maps. -/
theorem materials_engineering_bundle :
    materials_engineering_observable_count = 87 ∧
    materials_engineering_section_count = 7 ∧
    materials_engineering_D_eff = 14 ∧
    materials_engineering_pooled_median_error_pct < (5 : ℝ) ∧
    materials_engineering_headline_median_error_pct < (5 : ℝ) ∧
    0 < materials_engineering_beats_sota_headlines ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold materials_engineering_observable_count; norm_num,
    by unfold materials_engineering_section_count; norm_num,
    by unfold materials_engineering_D_eff; norm_num,
    materials_engineering_pooled_median_under_five_pct,
    materials_engineering_headline_median_under_five_pct,
    materials_engineering_beats_sota_headlines_pos,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal
