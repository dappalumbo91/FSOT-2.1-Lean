/-
  FSOT Formal AcousticResonanceMaterialsPriors — Acoustic_Resonance_Materials Tier L orbital gap fill.
  Generator: scripts/gen_tier_l_orbital_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def acoustic_rm_observable_count : ℕ := 29
def acoustic_rm_pooled_median_error_pct : ℝ := (0.008381497018412922 : ℝ)
def acoustic_rm_headline_median_error_pct : ℝ := (0.008381497018412922 : ℝ)
def acoustic_rm_beats_sota_headlines : ℕ := 3
def acoustic_rm_D_eff : ℕ := 15
def acoustic_rm_acoustic_species_count : ℕ := 9

theorem acoustic_rm_observable_count_pos : 0 < acoustic_rm_observable_count := by
  unfold acoustic_rm_observable_count; norm_num

theorem acoustic_rm_pooled_median_under_half_pct :
    acoustic_rm_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold acoustic_rm_pooled_median_error_pct; norm_num

theorem acoustic_rm_headline_median_under_half_pct :
    acoustic_rm_headline_median_error_pct < (0.5 : ℝ) := by
  unfold acoustic_rm_headline_median_error_pct; norm_num

theorem acoustic_rm_beats_sota_headlines_pos : 0 < acoustic_rm_beats_sota_headlines := by
  unfold acoustic_rm_beats_sota_headlines; norm_num
theorem acoustic_rm_acoustic_species_pos : 0 < acoustic_rm_acoustic_species_count := by unfold acoustic_rm_acoustic_species_count; norm_num

theorem acoustic_rm_bundle :
    acoustic_rm_observable_count = 29 ∧
    acoustic_rm_pooled_median_error_pct < (0.5 : ℝ) ∧
    acoustic_rm_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold acoustic_rm_observable_count; norm_num
  · exact acoustic_rm_pooled_median_under_half_pct
  · exact acoustic_rm_beats_sota_headlines_pos

end
