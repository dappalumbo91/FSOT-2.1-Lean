/-
  FSOT Formal BiologyStrictEmpiricalPriors — Tier 13 NCBI-grounded biology observables.
  Source: data/biology_strict_empirical.json (NC_012920.1)
  Generator: scripts/gen_biology_strict_empirical_lean.py
-/

import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

open Real

def biology_strict_observable_count : ℕ := 15
def biology_strict_operon_count : ℕ := 13
def biology_strict_median_error_pct : ℝ := (0.0 : ℝ)

theorem biology_strict_observable_count_pos : 0 < biology_strict_observable_count := by
  unfold biology_strict_observable_count; norm_num

theorem biology_strict_operon_count_pos : 0 < biology_strict_operon_count := by
  unfold biology_strict_operon_count; norm_num

theorem biology_strict_median_error_under_two_pct :
    biology_strict_median_error_pct < (2 : ℝ) := by
  unfold biology_strict_median_error_pct; norm_num

theorem biology_strict_bundle :
    biology_strict_observable_count = 15 ∧
    biology_strict_operon_count = 13 ∧
    biology_strict_median_error_pct < (2 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold biology_strict_observable_count; norm_num,
    by unfold biology_strict_operon_count; norm_num,
    biology_strict_median_error_under_two_pct,
    lab_biological_raw_S_positive
  ⟩

end

end FSOT.Formal
