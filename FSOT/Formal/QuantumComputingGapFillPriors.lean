/-
  FSOT Formal QuantumComputingGapFillPriors — Quantum_Computing tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_computing_gap_fill_observable_count : ℕ := 177
def quantum_computing_gap_fill_pooled_median_error_pct : ℝ := (0.0002953462072651492 : ℝ)
def quantum_computing_gap_fill_headline_median_error_pct : ℝ := (0.0002953462072651492 : ℝ)
def quantum_computing_gap_fill_beats_sota_headlines : ℕ := 2
def quantum_computing_gap_fill_D_eff : ℕ := 11

theorem quantum_computing_gap_fill_observable_count_pos : 0 < quantum_computing_gap_fill_observable_count := by
  unfold quantum_computing_gap_fill_observable_count; decide

theorem quantum_computing_gap_fill_pooled_median_under_half_pct :
    quantum_computing_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_computing_gap_fill_pooled_median_error_pct
  exact (by norm_num : (0.0002953462072651492  : ℝ) < 0.5)

theorem quantum_computing_gap_fill_headline_median_under_half_pct :
    quantum_computing_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_computing_gap_fill_headline_median_error_pct
  exact (by norm_num : (0.0002953462072651492  : ℝ) < 0.5)

theorem quantum_computing_gap_fill_beats_sota_headlines_pos : 0 < quantum_computing_gap_fill_beats_sota_headlines := by
  unfold quantum_computing_gap_fill_beats_sota_headlines; decide

theorem quantum_computing_gap_fill_bundle :
    quantum_computing_gap_fill_observable_count = 177 ∧
    quantum_computing_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    quantum_computing_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < quantum_computing_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold quantum_computing_gap_fill_observable_count; decide,
    quantum_computing_gap_fill_pooled_median_under_half_pct,
    quantum_computing_gap_fill_headline_median_under_half_pct,
    quantum_computing_gap_fill_beats_sota_headlines_pos,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
