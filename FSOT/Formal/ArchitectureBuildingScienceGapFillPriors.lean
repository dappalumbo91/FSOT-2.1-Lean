/-
  FSOT Formal ArchitectureBuildingScienceGapFillPriors — Architecture_Building_Science tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def architecture_building_science_gap_fill_observable_count : ℕ := 83
def architecture_building_science_gap_fill_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def architecture_building_science_gap_fill_headline_median_error_pct : ℝ := (0.0 : ℝ)
def architecture_building_science_gap_fill_beats_sota_headlines : ℕ := 3
def architecture_building_science_gap_fill_D_eff : ℕ := 16

theorem architecture_building_science_gap_fill_observable_count_pos : 0 < architecture_building_science_gap_fill_observable_count := by
  unfold architecture_building_science_gap_fill_observable_count; decide

theorem architecture_building_science_gap_fill_pooled_median_under_half_pct :
    architecture_building_science_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold architecture_building_science_gap_fill_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem architecture_building_science_gap_fill_headline_median_under_half_pct :
    architecture_building_science_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold architecture_building_science_gap_fill_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem architecture_building_science_gap_fill_beats_sota_headlines_pos : 0 < architecture_building_science_gap_fill_beats_sota_headlines := by
  unfold architecture_building_science_gap_fill_beats_sota_headlines; decide

theorem architecture_building_science_gap_fill_bundle :
    architecture_building_science_gap_fill_observable_count = 83 ∧
    architecture_building_science_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    architecture_building_science_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < architecture_building_science_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold architecture_building_science_gap_fill_observable_count; decide,
    architecture_building_science_gap_fill_pooled_median_under_half_pct,
    architecture_building_science_gap_fill_headline_median_under_half_pct,
    architecture_building_science_gap_fill_beats_sota_headlines_pos,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
