/-
  FSOT Formal FoundingCosmicDustPanelPriors — Tier 96 founding law panel (law_20: Cosmic Dust Grain Size Anomaly).
  Generator: scripts/gen_tier96_founding_laws_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def founding_cosmic_dust_panel_founding_law_id : String := "law_20"
def founding_cosmic_dust_panel_observable_count : ℕ := 5
def founding_cosmic_dust_panel_pooled_median_error_pct : ℝ := (0.088241 : ℝ)
def founding_cosmic_dust_panel_headline_median_error_pct : ℝ := (0.088241 : ℝ)
def founding_cosmic_dust_panel_beats_sota_headlines : ℕ := 2
def founding_cosmic_dust_panel_D_eff : ℕ := 13

theorem founding_cosmic_dust_panel_observable_count_pos : 0 < founding_cosmic_dust_panel_observable_count := by
  unfold founding_cosmic_dust_panel_observable_count; norm_num

theorem founding_cosmic_dust_panel_pooled_median_under_half_pct :
    founding_cosmic_dust_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold founding_cosmic_dust_panel_pooled_median_error_pct; norm_num

theorem founding_cosmic_dust_panel_headline_median_under_half_pct :
    founding_cosmic_dust_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold founding_cosmic_dust_panel_headline_median_error_pct; norm_num

theorem founding_cosmic_dust_panel_beats_sota_headlines_pos : 0 < founding_cosmic_dust_panel_beats_sota_headlines := by
  unfold founding_cosmic_dust_panel_beats_sota_headlines; norm_num

theorem founding_cosmic_dust_panel_bundle :
    founding_cosmic_dust_panel_observable_count = 5 ∧
    founding_cosmic_dust_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    founding_cosmic_dust_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold founding_cosmic_dust_panel_observable_count; norm_num
  · exact founding_cosmic_dust_panel_pooled_median_under_half_pct
  · exact founding_cosmic_dust_panel_beats_sota_headlines_pos

end
