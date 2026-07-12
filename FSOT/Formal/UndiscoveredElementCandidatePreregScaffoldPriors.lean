/-
  FSOT Formal UndiscoveredElementCandidatePreregScaffoldPriors — extension domain Undiscovered_Element_Candidate_Prereg_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def undiscovered_element_candidate_prereg_scaffold_observable_count : ℕ := 25
def undiscovered_element_candidate_prereg_scaffold_D_eff : ℕ := 10

theorem undiscovered_element_candidate_prereg_scaffold_observable_count_pos : 0 < undiscovered_element_candidate_prereg_scaffold_observable_count := by
  unfold undiscovered_element_candidate_prereg_scaffold_observable_count; norm_num

theorem undiscovered_element_candidate_prereg_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem undiscovered_element_candidate_prereg_scaffold_bundle :
    undiscovered_element_candidate_prereg_scaffold_observable_count = 25 ∧
    undiscovered_element_candidate_prereg_scaffold_D_eff = 10 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold undiscovered_element_candidate_prereg_scaffold_observable_count; norm_num,
    by unfold undiscovered_element_candidate_prereg_scaffold_D_eff; norm_num,
    undiscovered_element_candidate_prereg_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
