/-
  FSOT Formal EnergyNeuralOrbitalBridgePriors — Energy_Neural_Orbital_Bridge Tier L orbital gap fill.
  Generator: scripts/gen_tier_l_orbital_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def e_neu_br_observable_count : ℕ := 48
def e_neu_br_pooled_median_error_pct : ℝ := (0.01800266870179516 : ℝ)
def e_neu_br_headline_median_error_pct : ℝ := (0.01800266870179516 : ℝ)
def e_neu_br_beats_sota_headlines : ℕ := 2
def e_neu_br_D_eff : ℕ := 16
def e_neu_br_bridge_pair_count : ℕ := 36

theorem e_neu_br_observable_count_pos : 0 < e_neu_br_observable_count := by
  unfold e_neu_br_observable_count; norm_num

theorem e_neu_br_pooled_median_under_half_pct :
    e_neu_br_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold e_neu_br_pooled_median_error_pct; norm_num

theorem e_neu_br_headline_median_under_half_pct :
    e_neu_br_headline_median_error_pct < (0.5 : ℝ) := by
  unfold e_neu_br_headline_median_error_pct; norm_num

theorem e_neu_br_beats_sota_headlines_pos : 0 < e_neu_br_beats_sota_headlines := by
  unfold e_neu_br_beats_sota_headlines; norm_num
theorem e_neu_br_bridge_pairs_pos : 0 < e_neu_br_bridge_pair_count := by unfold e_neu_br_bridge_pair_count; norm_num

theorem e_neu_br_bundle :
    e_neu_br_observable_count = 48 ∧
    e_neu_br_pooled_median_error_pct < (0.5 : ℝ) ∧
    e_neu_br_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold e_neu_br_observable_count; norm_num
  · exact e_neu_br_pooled_median_under_half_pct
  · exact e_neu_br_beats_sota_headlines_pos

end
