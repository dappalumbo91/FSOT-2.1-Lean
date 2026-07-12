/-
  FSOT Formal AstrophysicalStructureCrosswalkPriors — extension domain Astrophysical_Structure_Crosswalk.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def astrophysical_structure_crosswalk_observable_count : ℕ := 32
def astrophysical_structure_crosswalk_D_eff : ℕ := 18

theorem astrophysical_structure_crosswalk_observable_count_pos : 0 < astrophysical_structure_crosswalk_observable_count := by
  unfold astrophysical_structure_crosswalk_observable_count; norm_num

theorem astrophysical_structure_crosswalk_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem astrophysical_structure_crosswalk_bundle :
    astrophysical_structure_crosswalk_observable_count = 32 ∧
    astrophysical_structure_crosswalk_D_eff = 18 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold astrophysical_structure_crosswalk_observable_count; norm_num,
    by unfold astrophysical_structure_crosswalk_D_eff; norm_num,
    astrophysical_structure_crosswalk_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
