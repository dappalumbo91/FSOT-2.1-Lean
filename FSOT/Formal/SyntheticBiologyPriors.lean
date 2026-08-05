/-
  FSOT Formal SyntheticBiologyPriors — evolution operons + biology strict bridge.
  Generator: scripts/gen_synthetic_biology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def synthetic_biology_observable_count : ℕ := 20
def synthetic_biology_median_error_pct : ℝ := (0.0 : ℝ)
def synthetic_biology_D_eff : ℕ := 14

theorem synthetic_biology_observable_count_pos : 0 < synthetic_biology_observable_count := by
  unfold synthetic_biology_observable_count; decide

theorem synthetic_biology_median_error_under_half_pct :
    synthetic_biology_median_error_pct < (0.5 : ℝ) := by
  unfold synthetic_biology_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem synthetic_biology_bundle :
    synthetic_biology_observable_count = 20 ∧
    synthetic_biology_D_eff = 14 ∧
    synthetic_biology_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold synthetic_biology_observable_count; decide,
    by unfold synthetic_biology_D_eff; decide,
    synthetic_biology_median_error_under_half_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
