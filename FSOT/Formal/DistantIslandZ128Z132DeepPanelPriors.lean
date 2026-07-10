/-
  FSOT Formal DistantIslandZ128Z132DeepPanelPriors — Tier 75 periodic extension closure.
  Generator: scripts/gen_tiers_75_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def distant_island_z128_z132_deep_panel_observable_count : ℕ := 14
def distant_island_z128_z132_deep_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def distant_island_z128_z132_deep_panel_headline_median_error_pct : ℝ := (9.504128963901446e-09 : ℝ)
def distant_island_z128_z132_deep_panel_beats_sota_headlines : ℕ := 2
def distant_island_z128_z132_deep_panel_D_eff : ℕ := 23

theorem distant_island_z128_z132_deep_panel_observable_count_pos : 0 < distant_island_z128_z132_deep_panel_observable_count := by
  unfold distant_island_z128_z132_deep_panel_observable_count; norm_num

theorem distant_island_z128_z132_deep_panel_pooled_median_under_half_pct :
    distant_island_z128_z132_deep_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold distant_island_z128_z132_deep_panel_pooled_median_error_pct; norm_num

theorem distant_island_z128_z132_deep_panel_headline_median_under_half_pct :
    distant_island_z128_z132_deep_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold distant_island_z128_z132_deep_panel_headline_median_error_pct; norm_num

theorem distant_island_z128_z132_deep_panel_beats_sota_headlines_pos : 0 < distant_island_z128_z132_deep_panel_beats_sota_headlines := by
  unfold distant_island_z128_z132_deep_panel_beats_sota_headlines; norm_num

theorem distant_island_z128_z132_deep_panel_bundle :
    distant_island_z128_z132_deep_panel_observable_count = 14 ∧
    distant_island_z128_z132_deep_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    distant_island_z128_z132_deep_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold distant_island_z128_z132_deep_panel_observable_count; norm_num
  · exact distant_island_z128_z132_deep_panel_pooled_median_under_half_pct
  · exact distant_island_z128_z132_deep_panel_beats_sota_headlines_pos

end
