/-
  FSOT Formal ParticleNeuralOrbitalBridgePriors — Particle_Neural_Orbital_Bridge Tier L orbital gap fill.
  Generator: scripts/gen_tier_l_orbital_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def p_neu_br_observable_count : ℕ := 48
def p_neu_br_pooled_median_error_pct : ℝ := (0.03326447040434832 : ℝ)
def p_neu_br_headline_median_error_pct : ℝ := (0.03326447040434832 : ℝ)
def p_neu_br_beats_sota_headlines : ℕ := 2
def p_neu_br_D_eff : ℕ := 17
def p_neu_br_bridge_pair_count : ℕ := 36

theorem p_neu_br_observable_count_pos : 0 < p_neu_br_observable_count := by
  unfold p_neu_br_observable_count; norm_num

theorem p_neu_br_pooled_median_under_half_pct :
    p_neu_br_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold p_neu_br_pooled_median_error_pct; norm_num

theorem p_neu_br_headline_median_under_half_pct :
    p_neu_br_headline_median_error_pct < (0.5 : ℝ) := by
  unfold p_neu_br_headline_median_error_pct; norm_num

theorem p_neu_br_beats_sota_headlines_pos : 0 < p_neu_br_beats_sota_headlines := by
  unfold p_neu_br_beats_sota_headlines; norm_num
theorem p_neu_br_bridge_pairs_pos : 0 < p_neu_br_bridge_pair_count := by unfold p_neu_br_bridge_pair_count; norm_num

theorem p_neu_br_bundle :
    p_neu_br_observable_count = 48 ∧
    p_neu_br_pooled_median_error_pct < (0.5 : ℝ) ∧
    p_neu_br_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold p_neu_br_observable_count; norm_num
  · exact p_neu_br_pooled_median_under_half_pct
  · exact p_neu_br_beats_sota_headlines_pos

end
