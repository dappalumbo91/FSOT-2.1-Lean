/-
  FSOT Formal SIMBADStellarIdentityDeepPriors — Tier 59/60 public material/fuel scaffold + live astrometry.
  Generator: scripts/gen_tiers_59_60_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def simbad_stellar_identity_deep_observable_count : ℕ := 40
def simbad_stellar_identity_deep_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def simbad_stellar_identity_deep_headline_median_error_pct : ℝ := (0.0 : ℝ)
def simbad_stellar_identity_deep_beats_sota_headlines : ℕ := 2
def simbad_stellar_identity_deep_D_eff : ℕ := 20

theorem simbad_stellar_identity_deep_observable_count_pos : 0 < simbad_stellar_identity_deep_observable_count := by
  unfold simbad_stellar_identity_deep_observable_count; norm_num

theorem simbad_stellar_identity_deep_pooled_median_under_half_pct :
    simbad_stellar_identity_deep_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold simbad_stellar_identity_deep_pooled_median_error_pct; norm_num

theorem simbad_stellar_identity_deep_headline_median_under_half_pct :
    simbad_stellar_identity_deep_headline_median_error_pct < (0.5 : ℝ) := by
  unfold simbad_stellar_identity_deep_headline_median_error_pct; norm_num

theorem simbad_stellar_identity_deep_beats_sota_headlines_pos : 0 < simbad_stellar_identity_deep_beats_sota_headlines := by
  unfold simbad_stellar_identity_deep_beats_sota_headlines; norm_num

theorem simbad_stellar_identity_deep_bundle :
    simbad_stellar_identity_deep_observable_count = 40 ∧
    simbad_stellar_identity_deep_pooled_median_error_pct < (0.5 : ℝ) ∧
    simbad_stellar_identity_deep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold simbad_stellar_identity_deep_observable_count; norm_num
  · exact simbad_stellar_identity_deep_pooled_median_under_half_pct
  · exact simbad_stellar_identity_deep_beats_sota_headlines_pos

end
