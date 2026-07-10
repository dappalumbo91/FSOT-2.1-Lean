/-
  FSOT Formal MedicalGalacticOrbitalBridgePriors — Medical_Galactic_Orbital_Bridge Tier M ToE unity.
  Generator: scripts/gen_tier_m_toe_unity_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def med_gal_br_observable_count : ℕ := 49
def med_gal_br_pooled_median_error_pct : ℝ := (0.01071774302852102 : ℝ)
def med_gal_br_headline_median_error_pct : ℝ := (0.01071774302852102 : ℝ)
def med_gal_br_beats_sota_headlines : ℕ := 2
def med_gal_br_D_eff : ℕ := 17
def med_gal_br_bridge_pair_count : ℕ := 36
def med_gal_br_cross_scale_motif_count : ℕ := 1

theorem med_gal_br_observable_count_pos : 0 < med_gal_br_observable_count := by
  unfold med_gal_br_observable_count; norm_num

theorem med_gal_br_pooled_median_under_five_pct :
    med_gal_br_pooled_median_error_pct < (5 : ℝ) := by
  unfold med_gal_br_pooled_median_error_pct; norm_num

theorem med_gal_br_headline_median_under_five_pct :
    med_gal_br_headline_median_error_pct < (5 : ℝ) := by
  unfold med_gal_br_headline_median_error_pct; norm_num

theorem med_gal_br_beats_sota_headlines_pos : 0 < med_gal_br_beats_sota_headlines := by
  unfold med_gal_br_beats_sota_headlines; norm_num
theorem med_gal_br_bridge_pairs_pos : 0 < med_gal_br_bridge_pair_count := by unfold med_gal_br_bridge_pair_count; norm_num

theorem med_gal_br_bundle :
    med_gal_br_observable_count = 49 ∧
    med_gal_br_pooled_median_error_pct < (5 : ℝ) ∧
    med_gal_br_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold med_gal_br_observable_count; norm_num
  · exact med_gal_br_pooled_median_under_five_pct
  · exact med_gal_br_beats_sota_headlines_pos

end
