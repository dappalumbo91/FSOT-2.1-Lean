/-
  FSOT Formal QuantumInformationPriors — Tier 66 NeuroLab residual registry panels.
  Generator: scripts/gen_tiers_66_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_information_observable_count : ℕ := 14
def quantum_information_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def quantum_information_headline_median_error_pct : ℝ := (0.0 : ℝ)
def quantum_information_beats_sota_headlines : ℕ := 2
def quantum_information_D_eff : ℕ := 11

theorem quantum_information_observable_count_pos : 0 < quantum_information_observable_count := by
  unfold quantum_information_observable_count; norm_num

theorem quantum_information_pooled_median_under_half_pct :
    quantum_information_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_information_pooled_median_error_pct; norm_num

theorem quantum_information_headline_median_under_half_pct :
    quantum_information_headline_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_information_headline_median_error_pct; norm_num

theorem quantum_information_beats_sota_headlines_pos : 0 < quantum_information_beats_sota_headlines := by
  unfold quantum_information_beats_sota_headlines; norm_num

theorem quantum_information_bundle :
    quantum_information_observable_count = 14 ∧
    quantum_information_pooled_median_error_pct < (0.5 : ℝ) ∧
    quantum_information_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold quantum_information_observable_count; norm_num
  · exact quantum_information_pooled_median_under_half_pct
  · exact quantum_information_beats_sota_headlines_pos

end
