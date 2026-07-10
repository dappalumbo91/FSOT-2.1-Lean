/-
  FSOT Formal MaterialsGenomeCrosswalkPriors — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def materials_genome_crosswalk_observable_count : ℕ := 38
def materials_genome_crosswalk_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def materials_genome_crosswalk_headline_median_error_pct : ℝ := (0.013419257571482188 : ℝ)
def materials_genome_crosswalk_beats_sota_headlines : ℕ := 2
def materials_genome_crosswalk_D_eff : ℕ := 15

theorem materials_genome_crosswalk_observable_count_pos : 0 < materials_genome_crosswalk_observable_count := by
  unfold materials_genome_crosswalk_observable_count; norm_num

theorem materials_genome_crosswalk_pooled_median_under_half_pct :
    materials_genome_crosswalk_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold materials_genome_crosswalk_pooled_median_error_pct; norm_num

theorem materials_genome_crosswalk_headline_median_under_half_pct :
    materials_genome_crosswalk_headline_median_error_pct < (0.5 : ℝ) := by
  unfold materials_genome_crosswalk_headline_median_error_pct; norm_num

theorem materials_genome_crosswalk_beats_sota_headlines_pos : 0 < materials_genome_crosswalk_beats_sota_headlines := by
  unfold materials_genome_crosswalk_beats_sota_headlines; norm_num

theorem materials_genome_crosswalk_bundle :
    materials_genome_crosswalk_observable_count = 38 ∧
    materials_genome_crosswalk_pooled_median_error_pct < (0.5 : ℝ) ∧
    materials_genome_crosswalk_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold materials_genome_crosswalk_observable_count; norm_num
  · exact materials_genome_crosswalk_pooled_median_under_half_pct
  · exact materials_genome_crosswalk_beats_sota_headlines_pos

end
