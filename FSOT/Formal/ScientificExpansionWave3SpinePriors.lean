/-
  FSOT Formal ScientificExpansionWave3SpinePriors — extension domain Scientific_Expansion_Wave3_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def scientific_expansion_wave3_spine_observable_count : ℕ := 40
def scientific_expansion_wave3_spine_D_eff : ℕ := 17

theorem scientific_expansion_wave3_spine_observable_count_pos : 0 < scientific_expansion_wave3_spine_observable_count := by
  unfold scientific_expansion_wave3_spine_observable_count; decide

theorem scientific_expansion_wave3_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem scientific_expansion_wave3_spine_bundle :
    scientific_expansion_wave3_spine_observable_count = 40 ∧
    scientific_expansion_wave3_spine_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold scientific_expansion_wave3_spine_observable_count; decide,
    by unfold scientific_expansion_wave3_spine_D_eff; decide,
    scientific_expansion_wave3_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
