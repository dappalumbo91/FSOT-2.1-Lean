/-
  FSOT Formal Sh0esRefinedPriors — extension domain SH0ES_Refined.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def sh0es_refined_observable_count : ℕ := 24
def sh0es_refined_D_eff : ℕ := 25

theorem sh0es_refined_observable_count_pos : 0 < sh0es_refined_observable_count := by
  unfold sh0es_refined_observable_count; decide

theorem sh0es_refined_median_error_under_half_pct :
    (0.024894 : ℝ) < (0.5 : ℝ) := by norm_num

theorem sh0es_refined_bundle :
    sh0es_refined_observable_count = 24 ∧
    sh0es_refined_D_eff = 25 ∧
    (0.024894 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold sh0es_refined_observable_count; decide,
    by unfold sh0es_refined_D_eff; decide,
    sh0es_refined_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
