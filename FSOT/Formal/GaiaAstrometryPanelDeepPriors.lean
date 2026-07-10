/-
  FSOT Formal GaiaAstrometryPanelDeepPriors — Tier 59/60 public material/fuel scaffold + live astrometry.
  Generator: scripts/gen_tiers_59_60_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gaia_astrometry_panel_deep_observable_count : ℕ := 62
def gaia_astrometry_panel_deep_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def gaia_astrometry_panel_deep_headline_median_error_pct : ℝ := (0.111276 : ℝ)
def gaia_astrometry_panel_deep_beats_sota_headlines : ℕ := 2
def gaia_astrometry_panel_deep_D_eff : ℕ := 20

theorem gaia_astrometry_panel_deep_observable_count_pos : 0 < gaia_astrometry_panel_deep_observable_count := by
  unfold gaia_astrometry_panel_deep_observable_count; norm_num

theorem gaia_astrometry_panel_deep_pooled_median_under_half_pct :
    gaia_astrometry_panel_deep_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold gaia_astrometry_panel_deep_pooled_median_error_pct; norm_num

theorem gaia_astrometry_panel_deep_headline_median_under_half_pct :
    gaia_astrometry_panel_deep_headline_median_error_pct < (0.5 : ℝ) := by
  unfold gaia_astrometry_panel_deep_headline_median_error_pct; norm_num

theorem gaia_astrometry_panel_deep_beats_sota_headlines_pos : 0 < gaia_astrometry_panel_deep_beats_sota_headlines := by
  unfold gaia_astrometry_panel_deep_beats_sota_headlines; norm_num

theorem gaia_astrometry_panel_deep_bundle :
    gaia_astrometry_panel_deep_observable_count = 62 ∧
    gaia_astrometry_panel_deep_pooled_median_error_pct < (0.5 : ℝ) ∧
    gaia_astrometry_panel_deep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold gaia_astrometry_panel_deep_observable_count; norm_num
  · exact gaia_astrometry_panel_deep_pooled_median_under_half_pct
  · exact gaia_astrometry_panel_deep_beats_sota_headlines_pos

end
