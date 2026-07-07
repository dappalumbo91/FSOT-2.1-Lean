/-
  FSOT Formal IGEMSyntheticBiologyPriors — iGEM parts-registry strict-empirical bridge.
  Generator: scripts/gen_igem_synthetic_biology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def igem_synthetic_biology_observable_count : ℕ := 60
def igem_synthetic_biology_median_error_pct : ℝ := (0.04447250077037545 : ℝ)
def igem_synthetic_biology_D_eff : ℕ := 14

theorem igem_synthetic_biology_observable_count_pos : 0 < igem_synthetic_biology_observable_count := by
  unfold igem_synthetic_biology_observable_count; norm_num

theorem igem_synthetic_biology_median_error_under_five_pct :
    igem_synthetic_biology_median_error_pct < (5 : ℝ) := by
  unfold igem_synthetic_biology_median_error_pct; norm_num

theorem igem_synthetic_biology_bundle :
    igem_synthetic_biology_observable_count = 60 ∧
    igem_synthetic_biology_D_eff = 14 ∧
    igem_synthetic_biology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold igem_synthetic_biology_observable_count; norm_num,
    by unfold igem_synthetic_biology_D_eff; norm_num,
    igem_synthetic_biology_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
