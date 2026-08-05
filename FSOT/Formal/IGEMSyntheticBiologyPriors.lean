/-
  FSOT Formal IGEMSyntheticBiologyPriors — iGEM parts-registry strict-empirical bridge.
  Generator: scripts/gen_igem_synthetic_biology_lean.py
  Source: vendor/igem
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def igem_synthetic_biology_observable_count : ℕ := 54
def igem_synthetic_biology_part_count : ℕ := 20
def igem_synthetic_biology_D_eff : ℕ := 14
def igem_synthetic_biology_pooled_median_error_pct : ℝ := (0.022236250385203583 : ℝ)
def igem_synthetic_biology_headline_median_error_pct : ℝ := (0.022236250385203583 : ℝ)
def igem_synthetic_biology_beats_sota_headlines : ℕ := 6

theorem igem_synthetic_biology_observable_count_pos : 0 < igem_synthetic_biology_observable_count := by
  unfold igem_synthetic_biology_observable_count; decide

theorem igem_synthetic_biology_part_count_pos : 0 < igem_synthetic_biology_part_count := by
  unfold igem_synthetic_biology_part_count; decide

theorem igem_synthetic_biology_pooled_median_under_half_pct :
    igem_synthetic_biology_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold igem_synthetic_biology_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem igem_synthetic_biology_headline_median_under_half_pct :
    igem_synthetic_biology_headline_median_error_pct < (0.5 : ℝ) := by
  unfold igem_synthetic_biology_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem igem_synthetic_biology_beats_sota_headlines_pos : 0 < igem_synthetic_biology_beats_sota_headlines := by
  unfold igem_synthetic_biology_beats_sota_headlines; decide

theorem igem_synthetic_biology_bundle :
    igem_synthetic_biology_observable_count = 54 ∧
    igem_synthetic_biology_part_count = 20 ∧
    igem_synthetic_biology_D_eff = 14 ∧
    igem_synthetic_biology_pooled_median_error_pct < (0.5 : ℝ) ∧
    igem_synthetic_biology_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < igem_synthetic_biology_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold igem_synthetic_biology_observable_count; decide,
    by unfold igem_synthetic_biology_part_count; decide,
    by unfold igem_synthetic_biology_D_eff; decide,
    igem_synthetic_biology_pooled_median_under_half_pct,
    igem_synthetic_biology_headline_median_under_half_pct,
    igem_synthetic_biology_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal
