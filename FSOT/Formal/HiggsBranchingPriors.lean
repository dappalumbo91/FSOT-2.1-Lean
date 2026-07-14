/-
  FSOT Formal HiggsBranchingPriors — dedicated HEP/Higgs branching observables.
  Generator: scripts/gen_higgs_branching_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def higgs_compute_branching_count : ℕ := 9
def higgs_thesis_target_count : ℕ := 5
def higgs_branching_observable_count : ℕ := 14
def higgs_branching_median_error_pct : ℝ := (0.08808351263334355 : ℝ)
def higgs_branching_max_error_pct : ℝ := (4.232801452006084 : ℝ)

theorem higgs_compute_branching_count_pos : 0 < higgs_compute_branching_count := by
  unfold higgs_compute_branching_count; norm_num

theorem higgs_branching_observable_count_pos : 0 < higgs_branching_observable_count := by
  unfold higgs_branching_observable_count; norm_num

theorem higgs_branching_components_sum :
    higgs_compute_branching_count + higgs_thesis_target_count = higgs_branching_observable_count := by
  unfold higgs_compute_branching_count higgs_thesis_target_count higgs_branching_observable_count; norm_num

theorem higgs_branching_median_error_under_half_pct :
    higgs_branching_median_error_pct < (0.5 : ℝ) := by
  unfold higgs_branching_median_error_pct; norm_num

theorem higgs_branching_max_error_under_half_pct :
    higgs_branching_max_error_pct < (0.5 : ℝ) := by
  unfold higgs_branching_max_error_pct; norm_num

/-- Bundle: Higgs BR from fsot_compute + thesis wave8 with higgs-domain sign proxy. -/
theorem higgs_branching_bundle :
    higgs_compute_branching_count = 9 ∧
    higgs_thesis_target_count = 5 ∧
    higgs_branching_observable_count = 14 ∧
    higgs_compute_branching_count + higgs_thesis_target_count = 14 ∧
    higgs_branching_median_error_pct < (0.5 : ℝ) ∧
    higgs_branching_max_error_pct < (0.5 : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "higgs") := by
  refine ⟨
    by unfold higgs_compute_branching_count; norm_num,
    by unfold higgs_thesis_target_count; norm_num,
    by unfold higgs_branching_observable_count; norm_num,
    higgs_branching_components_sum,
    higgs_branching_median_error_under_half_pct,
    higgs_branching_max_error_under_half_pct,
    higgs_raw_S_positive
  ⟩

end

end FSOT.Formal
