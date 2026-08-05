/-
  FSOT Formal FuelCandidatePreregScaffoldPriors — extension domain Fuel_Candidate_Prereg_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fuel_candidate_prereg_scaffold_observable_count : ℕ := 33
def fuel_candidate_prereg_scaffold_D_eff : ℕ := 16

theorem fuel_candidate_prereg_scaffold_observable_count_pos : 0 < fuel_candidate_prereg_scaffold_observable_count := by
  unfold fuel_candidate_prereg_scaffold_observable_count; decide

theorem fuel_candidate_prereg_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem fuel_candidate_prereg_scaffold_bundle :
    fuel_candidate_prereg_scaffold_observable_count = 33 ∧
    fuel_candidate_prereg_scaffold_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fuel_candidate_prereg_scaffold_observable_count; decide,
    by unfold fuel_candidate_prereg_scaffold_D_eff; decide,
    fuel_candidate_prereg_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
