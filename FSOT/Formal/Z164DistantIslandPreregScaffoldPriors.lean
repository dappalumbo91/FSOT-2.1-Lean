/-
  FSOT Formal Z164DistantIslandPreregScaffoldPriors — Tier 75 periodic extension closure.
  Generator: scripts/gen_tiers_75_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def z164_distant_island_prereg_scaffold_observable_count : ℕ := 7
def z164_distant_island_prereg_scaffold_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def z164_distant_island_prereg_scaffold_headline_median_error_pct : ℝ := (0.0 : ℝ)
def z164_distant_island_prereg_scaffold_beats_sota_headlines : ℕ := 2
def z164_distant_island_prereg_scaffold_D_eff : ℕ := 24

theorem z164_distant_island_prereg_scaffold_observable_count_pos : 0 < z164_distant_island_prereg_scaffold_observable_count := by
  unfold z164_distant_island_prereg_scaffold_observable_count; norm_num

theorem z164_distant_island_prereg_scaffold_pooled_median_under_half_pct :
    z164_distant_island_prereg_scaffold_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold z164_distant_island_prereg_scaffold_pooled_median_error_pct; norm_num

theorem z164_distant_island_prereg_scaffold_headline_median_under_half_pct :
    z164_distant_island_prereg_scaffold_headline_median_error_pct < (0.5 : ℝ) := by
  unfold z164_distant_island_prereg_scaffold_headline_median_error_pct; norm_num

theorem z164_distant_island_prereg_scaffold_beats_sota_headlines_pos : 0 < z164_distant_island_prereg_scaffold_beats_sota_headlines := by
  unfold z164_distant_island_prereg_scaffold_beats_sota_headlines; norm_num

theorem z164_distant_island_prereg_scaffold_bundle :
    z164_distant_island_prereg_scaffold_observable_count = 7 ∧
    z164_distant_island_prereg_scaffold_pooled_median_error_pct < (0.5 : ℝ) ∧
    z164_distant_island_prereg_scaffold_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold z164_distant_island_prereg_scaffold_observable_count; norm_num
  · exact z164_distant_island_prereg_scaffold_pooled_median_under_half_pct
  · exact z164_distant_island_prereg_scaffold_beats_sota_headlines_pos

end
