/-
  FSOT Formal StellarMultiplicityCatalogPriors — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def stellar_multiplicity_catalog_observable_count : ℕ := 68
def stellar_multiplicity_catalog_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def stellar_multiplicity_catalog_headline_median_error_pct : ℝ := (0.0 : ℝ)
def stellar_multiplicity_catalog_beats_sota_headlines : ℕ := 2
def stellar_multiplicity_catalog_D_eff : ℕ := 19

theorem stellar_multiplicity_catalog_observable_count_pos : 0 < stellar_multiplicity_catalog_observable_count := by
  unfold stellar_multiplicity_catalog_observable_count; norm_num

theorem stellar_multiplicity_catalog_pooled_median_under_half_pct :
    stellar_multiplicity_catalog_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold stellar_multiplicity_catalog_pooled_median_error_pct; norm_num

theorem stellar_multiplicity_catalog_headline_median_under_half_pct :
    stellar_multiplicity_catalog_headline_median_error_pct < (0.5 : ℝ) := by
  unfold stellar_multiplicity_catalog_headline_median_error_pct; norm_num

theorem stellar_multiplicity_catalog_beats_sota_headlines_pos : 0 < stellar_multiplicity_catalog_beats_sota_headlines := by
  unfold stellar_multiplicity_catalog_beats_sota_headlines; norm_num

theorem stellar_multiplicity_catalog_bundle :
    stellar_multiplicity_catalog_observable_count = 68 ∧
    stellar_multiplicity_catalog_pooled_median_error_pct < (0.5 : ℝ) ∧
    stellar_multiplicity_catalog_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold stellar_multiplicity_catalog_observable_count; norm_num
  · exact stellar_multiplicity_catalog_pooled_median_under_half_pct
  · exact stellar_multiplicity_catalog_beats_sota_headlines_pos

end
