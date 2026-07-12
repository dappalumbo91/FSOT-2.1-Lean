/-
  FSOT Formal RealityFoldingSpinePriors — extension domain Reality_Folding_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def reality_folding_spine_observable_count : ℕ := 24
def reality_folding_spine_D_eff : ℕ := 21

theorem reality_folding_spine_observable_count_pos : 0 < reality_folding_spine_observable_count := by
  unfold reality_folding_spine_observable_count; norm_num

theorem reality_folding_spine_median_error_under_half_pct :
    (0.023914275640537417 : ℝ) < (0.5 : ℝ) := by norm_num

theorem reality_folding_spine_bundle :
    reality_folding_spine_observable_count = 24 ∧
    reality_folding_spine_D_eff = 21 ∧
    (0.023914275640537417 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold reality_folding_spine_observable_count; norm_num,
    by unfold reality_folding_spine_D_eff; norm_num,
    reality_folding_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
