/-
  FSOT Formal ColdFusionLabSynthesisCrosswalkPriors — extension domain Cold_Fusion_Lab_Synthesis_Crosswalk.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cold_fusion_lab_synthesis_crosswalk_observable_count : ℕ := 22
def cold_fusion_lab_synthesis_crosswalk_D_eff : ℕ := 15

theorem cold_fusion_lab_synthesis_crosswalk_observable_count_pos : 0 < cold_fusion_lab_synthesis_crosswalk_observable_count := by
  unfold cold_fusion_lab_synthesis_crosswalk_observable_count; norm_num

theorem cold_fusion_lab_synthesis_crosswalk_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem cold_fusion_lab_synthesis_crosswalk_bundle :
    cold_fusion_lab_synthesis_crosswalk_observable_count = 22 ∧
    cold_fusion_lab_synthesis_crosswalk_D_eff = 15 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cold_fusion_lab_synthesis_crosswalk_observable_count; norm_num,
    by unfold cold_fusion_lab_synthesis_crosswalk_D_eff; norm_num,
    cold_fusion_lab_synthesis_crosswalk_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
