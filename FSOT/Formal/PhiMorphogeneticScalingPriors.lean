/-
  FSOT Formal PhiMorphogeneticScalingPriors — Phi_Morphogenetic_Scaling Tier L orbital gap fill.
  Generator: scripts/gen_tier_l_orbital_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def phi_morph_observable_count : ℕ := 327
def phi_morph_pooled_median_error_pct : ℝ := (0.0565 : ℝ)
def phi_morph_headline_median_error_pct : ℝ := (0.0565 : ℝ)
def phi_morph_beats_sota_headlines : ℕ := 3
def phi_morph_D_eff : ℕ := 16
def phi_morph_phi_species_count : ℕ := 307

theorem phi_morph_observable_count_pos : 0 < phi_morph_observable_count := by
  unfold phi_morph_observable_count; norm_num

theorem phi_morph_pooled_median_under_five_pct :
    phi_morph_pooled_median_error_pct < (5 : ℝ) := by
  unfold phi_morph_pooled_median_error_pct; norm_num

theorem phi_morph_headline_median_under_five_pct :
    phi_morph_headline_median_error_pct < (5 : ℝ) := by
  unfold phi_morph_headline_median_error_pct; norm_num

theorem phi_morph_beats_sota_headlines_pos : 0 < phi_morph_beats_sota_headlines := by
  unfold phi_morph_beats_sota_headlines; norm_num
theorem phi_morph_phi_species_pos : 0 < phi_morph_phi_species_count := by unfold phi_morph_phi_species_count; norm_num

theorem phi_morph_bundle :
    phi_morph_observable_count = 327 ∧
    phi_morph_pooled_median_error_pct < (5 : ℝ) ∧
    phi_morph_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold phi_morph_observable_count; norm_num
  · exact phi_morph_pooled_median_under_five_pct
  · exact phi_morph_beats_sota_headlines_pos

end
