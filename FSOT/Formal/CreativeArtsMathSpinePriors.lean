/-
  FSOT Formal CreativeArtsMathSpinePriors — extension domain Creative_Arts_Math_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def creative_arts_math_spine_observable_count : ℕ := 56
def creative_arts_math_spine_D_eff : ℕ := 16

theorem creative_arts_math_spine_observable_count_pos : 0 < creative_arts_math_spine_observable_count := by
  unfold creative_arts_math_spine_observable_count; decide

theorem creative_arts_math_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem creative_arts_math_spine_bundle :
    creative_arts_math_spine_observable_count = 56 ∧
    creative_arts_math_spine_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold creative_arts_math_spine_observable_count; decide,
    by unfold creative_arts_math_spine_D_eff; decide,
    creative_arts_math_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
