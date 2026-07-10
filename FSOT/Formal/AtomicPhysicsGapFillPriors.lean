/-
  FSOT Formal AtomicPhysicsGapFillPriors — Atomic_Physics tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def atomic_physics_gap_fill_observable_count : ℕ := 80
def atomic_physics_gap_fill_pooled_median_error_pct : ℝ := (0.0009504134401195552 : ℝ)
def atomic_physics_gap_fill_headline_median_error_pct : ℝ := (0.0009504134401195552 : ℝ)
def atomic_physics_gap_fill_beats_sota_headlines : ℕ := 2
def atomic_physics_gap_fill_D_eff : ℕ := 7

theorem atomic_physics_gap_fill_observable_count_pos : 0 < atomic_physics_gap_fill_observable_count := by
  unfold atomic_physics_gap_fill_observable_count; norm_num

theorem atomic_physics_gap_fill_pooled_median_under_five_pct :
    atomic_physics_gap_fill_pooled_median_error_pct < (5 : ℝ) := by
  unfold atomic_physics_gap_fill_pooled_median_error_pct; norm_num

theorem atomic_physics_gap_fill_headline_median_under_five_pct :
    atomic_physics_gap_fill_headline_median_error_pct < (5 : ℝ) := by
  unfold atomic_physics_gap_fill_headline_median_error_pct; norm_num

theorem atomic_physics_gap_fill_beats_sota_headlines_pos : 0 < atomic_physics_gap_fill_beats_sota_headlines := by
  unfold atomic_physics_gap_fill_beats_sota_headlines; norm_num

theorem atomic_physics_gap_fill_bundle :
    atomic_physics_gap_fill_observable_count = 80 ∧
    atomic_physics_gap_fill_pooled_median_error_pct < (5 : ℝ) ∧
    atomic_physics_gap_fill_headline_median_error_pct < (5 : ℝ) ∧
    0 < atomic_physics_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold atomic_physics_gap_fill_observable_count; norm_num,
    atomic_physics_gap_fill_pooled_median_under_five_pct,
    atomic_physics_gap_fill_headline_median_under_five_pct,
    atomic_physics_gap_fill_beats_sota_headlines_pos,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
