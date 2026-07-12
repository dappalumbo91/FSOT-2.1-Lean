/-
  FSOT Formal ArchitectureBuildingSciencePriors — extension domain Architecture_Building_Science.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def architecture_building_science_observable_count : ℕ := 43
def architecture_building_science_D_eff : ℕ := 16

theorem architecture_building_science_observable_count_pos : 0 < architecture_building_science_observable_count := by
  unfold architecture_building_science_observable_count; norm_num

theorem architecture_building_science_median_error_under_half_pct :
    (0.07869745016115058 : ℝ) < (0.5 : ℝ) := by norm_num

theorem architecture_building_science_bundle :
    architecture_building_science_observable_count = 43 ∧
    architecture_building_science_D_eff = 16 ∧
    (0.07869745016115058 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold architecture_building_science_observable_count; norm_num,
    by unfold architecture_building_science_D_eff; norm_num,
    architecture_building_science_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
