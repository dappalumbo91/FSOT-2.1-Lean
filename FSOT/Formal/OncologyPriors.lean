/-
  FSOT Formal OncologyPriors — SMILES drug/enzyme + biology strict bridge.
  Generator: scripts/gen_oncology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def oncology_observable_count : ℕ := 67
def oncology_median_error_pct : ℝ := (0.280526 : ℝ)
def oncology_D_eff : ℕ := 14

theorem oncology_observable_count_pos : 0 < oncology_observable_count := by
  unfold oncology_observable_count; norm_num

theorem oncology_median_error_under_five_pct :
    oncology_median_error_pct < (5 : ℝ) := by
  unfold oncology_median_error_pct; norm_num

theorem oncology_bundle :
    oncology_observable_count = 67 ∧
    oncology_D_eff = 14 ∧
    oncology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold oncology_observable_count; norm_num,
    by unfold oncology_D_eff; norm_num,
    oncology_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
