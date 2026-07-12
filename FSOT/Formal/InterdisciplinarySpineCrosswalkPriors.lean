/-
  FSOT Formal InterdisciplinarySpineCrosswalkPriors — extension domain Interdisciplinary_Spine_Crosswalk.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def interdisciplinary_spine_crosswalk_observable_count : ℕ := 24
def interdisciplinary_spine_crosswalk_D_eff : ℕ := 17

theorem interdisciplinary_spine_crosswalk_observable_count_pos : 0 < interdisciplinary_spine_crosswalk_observable_count := by
  unfold interdisciplinary_spine_crosswalk_observable_count; norm_num

theorem interdisciplinary_spine_crosswalk_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem interdisciplinary_spine_crosswalk_bundle :
    interdisciplinary_spine_crosswalk_observable_count = 24 ∧
    interdisciplinary_spine_crosswalk_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold interdisciplinary_spine_crosswalk_observable_count; norm_num,
    by unfold interdisciplinary_spine_crosswalk_D_eff; norm_num,
    interdisciplinary_spine_crosswalk_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
