/-
  FSOT Formal QuantumMechanicsGapFillPriors — Quantum_Mechanics tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_mechanics_gap_fill_observable_count : ℕ := 50
def quantum_mechanics_gap_fill_pooled_median_error_pct : ℝ := (9.52387420324368e-05 : ℝ)
def quantum_mechanics_gap_fill_headline_median_error_pct : ℝ := (9.52387420324368e-05 : ℝ)
def quantum_mechanics_gap_fill_beats_sota_headlines : ℕ := 2
def quantum_mechanics_gap_fill_D_eff : ℕ := 6

theorem quantum_mechanics_gap_fill_observable_count_pos : 0 < quantum_mechanics_gap_fill_observable_count := by
  unfold quantum_mechanics_gap_fill_observable_count; norm_num

theorem quantum_mechanics_gap_fill_pooled_median_under_half_pct :
    quantum_mechanics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_mechanics_gap_fill_pooled_median_error_pct; norm_num

theorem quantum_mechanics_gap_fill_headline_median_under_half_pct :
    quantum_mechanics_gap_fill_headline_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_mechanics_gap_fill_headline_median_error_pct; norm_num

theorem quantum_mechanics_gap_fill_beats_sota_headlines_pos : 0 < quantum_mechanics_gap_fill_beats_sota_headlines := by
  unfold quantum_mechanics_gap_fill_beats_sota_headlines; norm_num

theorem quantum_mechanics_gap_fill_bundle :
    quantum_mechanics_gap_fill_observable_count = 50 ∧
    quantum_mechanics_gap_fill_pooled_median_error_pct < (0.5 : ℝ) ∧
    quantum_mechanics_gap_fill_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < quantum_mechanics_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "quantum") > 0 := by
  refine ⟨
    by unfold quantum_mechanics_gap_fill_observable_count; norm_num,
    quantum_mechanics_gap_fill_pooled_median_under_half_pct,
    quantum_mechanics_gap_fill_headline_median_under_half_pct,
    quantum_mechanics_gap_fill_beats_sota_headlines_pos,
    quantum_raw_S_positive
  ⟩

end

end FSOT.Formal
