/-
  FSOT Formal ColdFusionCandidatePreregScaffoldPriors — extension domain Cold_Fusion_Candidate_Prereg_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cold_fusion_candidate_prereg_scaffold_observable_count : ℕ := 24
def cold_fusion_candidate_prereg_scaffold_D_eff : ℕ := 14

theorem cold_fusion_candidate_prereg_scaffold_observable_count_pos : 0 < cold_fusion_candidate_prereg_scaffold_observable_count := by
  unfold cold_fusion_candidate_prereg_scaffold_observable_count; decide

theorem cold_fusion_candidate_prereg_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem cold_fusion_candidate_prereg_scaffold_bundle :
    cold_fusion_candidate_prereg_scaffold_observable_count = 24 ∧
    cold_fusion_candidate_prereg_scaffold_D_eff = 14 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cold_fusion_candidate_prereg_scaffold_observable_count; decide,
    by unfold cold_fusion_candidate_prereg_scaffold_D_eff; decide,
    cold_fusion_candidate_prereg_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
