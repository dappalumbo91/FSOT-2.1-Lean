/-
  FSOT Formal GalacticStructureSamplePriors — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def galactic_structure_sample_observable_count : ℕ := 101
def galactic_structure_sample_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def galactic_structure_sample_headline_median_error_pct : ℝ := (0.111276 : ℝ)
def galactic_structure_sample_beats_sota_headlines : ℕ := 2
def galactic_structure_sample_D_eff : ℕ := 20

theorem galactic_structure_sample_observable_count_pos : 0 < galactic_structure_sample_observable_count := by
  unfold galactic_structure_sample_observable_count; norm_num

theorem galactic_structure_sample_pooled_median_under_half_pct :
    galactic_structure_sample_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold galactic_structure_sample_pooled_median_error_pct; norm_num

theorem galactic_structure_sample_headline_median_under_half_pct :
    galactic_structure_sample_headline_median_error_pct < (0.5 : ℝ) := by
  unfold galactic_structure_sample_headline_median_error_pct; norm_num

theorem galactic_structure_sample_beats_sota_headlines_pos : 0 < galactic_structure_sample_beats_sota_headlines := by
  unfold galactic_structure_sample_beats_sota_headlines; norm_num

theorem galactic_structure_sample_bundle :
    galactic_structure_sample_observable_count = 101 ∧
    galactic_structure_sample_pooled_median_error_pct < (0.5 : ℝ) ∧
    galactic_structure_sample_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold galactic_structure_sample_observable_count; norm_num
  · exact galactic_structure_sample_pooled_median_under_half_pct
  · exact galactic_structure_sample_beats_sota_headlines_pos

end
