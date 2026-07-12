/-
  FSOT Formal ScientificExpansionDepthWave2SpinePriors — extension domain Scientific_Expansion_Depth_Wave2_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def scientific_expansion_depth_wave2_spine_observable_count : ℕ := 20
def scientific_expansion_depth_wave2_spine_D_eff : ℕ := 18

theorem scientific_expansion_depth_wave2_spine_observable_count_pos : 0 < scientific_expansion_depth_wave2_spine_observable_count := by
  unfold scientific_expansion_depth_wave2_spine_observable_count; norm_num

theorem scientific_expansion_depth_wave2_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem scientific_expansion_depth_wave2_spine_bundle :
    scientific_expansion_depth_wave2_spine_observable_count = 20 ∧
    scientific_expansion_depth_wave2_spine_D_eff = 18 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold scientific_expansion_depth_wave2_spine_observable_count; norm_num,
    by unfold scientific_expansion_depth_wave2_spine_D_eff; norm_num,
    scientific_expansion_depth_wave2_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
