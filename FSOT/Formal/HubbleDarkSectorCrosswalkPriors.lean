/-
  FSOT Formal HubbleDarkSectorCrosswalkPriors — Tier 76 fluid spacetime + cosmology.
  Generator: scripts/gen_tiers_76_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def hubble_dark_sector_crosswalk_observable_count : ℕ := 20
def hubble_dark_sector_crosswalk_pooled_median_error_pct : ℝ := (0.000502 : ℝ)
def hubble_dark_sector_crosswalk_headline_median_error_pct : ℝ := (0.0005024559462089657 : ℝ)
def hubble_dark_sector_crosswalk_beats_sota_headlines : ℕ := 2
def hubble_dark_sector_crosswalk_D_eff : ℕ := 25

theorem hubble_dark_sector_crosswalk_observable_count_pos : 0 < hubble_dark_sector_crosswalk_observable_count := by
  unfold hubble_dark_sector_crosswalk_observable_count; norm_num

theorem hubble_dark_sector_crosswalk_pooled_median_under_half_pct :
    hubble_dark_sector_crosswalk_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold hubble_dark_sector_crosswalk_pooled_median_error_pct; norm_num

theorem hubble_dark_sector_crosswalk_headline_median_under_half_pct :
    hubble_dark_sector_crosswalk_headline_median_error_pct < (0.5 : ℝ) := by
  unfold hubble_dark_sector_crosswalk_headline_median_error_pct; norm_num

theorem hubble_dark_sector_crosswalk_beats_sota_headlines_pos : 0 < hubble_dark_sector_crosswalk_beats_sota_headlines := by
  unfold hubble_dark_sector_crosswalk_beats_sota_headlines; norm_num

theorem hubble_dark_sector_crosswalk_bundle :
    hubble_dark_sector_crosswalk_observable_count = 20 ∧
    hubble_dark_sector_crosswalk_pooled_median_error_pct < (0.5 : ℝ) ∧
    hubble_dark_sector_crosswalk_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold hubble_dark_sector_crosswalk_observable_count; norm_num
  · exact hubble_dark_sector_crosswalk_pooled_median_under_half_pct
  · exact hubble_dark_sector_crosswalk_beats_sota_headlines_pos

end
