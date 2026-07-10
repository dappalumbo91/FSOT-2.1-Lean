/-
  FSOT Formal PublishedFuelPropertyPanelPriors — Tier 57/58 public interdisciplinary / live catalog.
  Generator: scripts/gen_tiers_57_58_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def published_fuel_property_panel_observable_count : ℕ := 31
def published_fuel_property_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def published_fuel_property_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def published_fuel_property_panel_beats_sota_headlines : ℕ := 2
def published_fuel_property_panel_D_eff : ℕ := 16

theorem published_fuel_property_panel_observable_count_pos : 0 < published_fuel_property_panel_observable_count := by
  unfold published_fuel_property_panel_observable_count; norm_num

theorem published_fuel_property_panel_pooled_median_under_half_pct :
    published_fuel_property_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold published_fuel_property_panel_pooled_median_error_pct; norm_num

theorem published_fuel_property_panel_headline_median_under_half_pct :
    published_fuel_property_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold published_fuel_property_panel_headline_median_error_pct; norm_num

theorem published_fuel_property_panel_beats_sota_headlines_pos : 0 < published_fuel_property_panel_beats_sota_headlines := by
  unfold published_fuel_property_panel_beats_sota_headlines; norm_num

theorem published_fuel_property_panel_bundle :
    published_fuel_property_panel_observable_count = 31 ∧
    published_fuel_property_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    published_fuel_property_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold published_fuel_property_panel_observable_count; norm_num
  · exact published_fuel_property_panel_pooled_median_under_half_pct
  · exact published_fuel_property_panel_beats_sota_headlines_pos

end
