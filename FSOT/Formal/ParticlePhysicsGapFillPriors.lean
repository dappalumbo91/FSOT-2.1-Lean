/-
  FSOT Formal ParticlePhysicsGapFillPriors — Particle_Physics tier gap-fill (real API anchors).
  Generator: scripts/gen_tier_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def particle_physics_gap_fill_observable_count : ℕ := 98
def particle_physics_gap_fill_pooled_median_error_pct : ℝ := (0.002729984252880815 : ℝ)
def particle_physics_gap_fill_headline_median_error_pct : ℝ := (0.002729984252880815 : ℝ)
def particle_physics_gap_fill_beats_sota_headlines : ℕ := 2
def particle_physics_gap_fill_D_eff : ℕ := 7

theorem particle_physics_gap_fill_observable_count_pos : 0 < particle_physics_gap_fill_observable_count := by
  unfold particle_physics_gap_fill_observable_count; norm_num

theorem particle_physics_gap_fill_pooled_median_under_five_pct :
    particle_physics_gap_fill_pooled_median_error_pct < (5 : ℝ) := by
  unfold particle_physics_gap_fill_pooled_median_error_pct; norm_num

theorem particle_physics_gap_fill_headline_median_under_five_pct :
    particle_physics_gap_fill_headline_median_error_pct < (5 : ℝ) := by
  unfold particle_physics_gap_fill_headline_median_error_pct; norm_num

theorem particle_physics_gap_fill_beats_sota_headlines_pos : 0 < particle_physics_gap_fill_beats_sota_headlines := by
  unfold particle_physics_gap_fill_beats_sota_headlines; norm_num

theorem particle_physics_gap_fill_bundle :
    particle_physics_gap_fill_observable_count = 98 ∧
    particle_physics_gap_fill_pooled_median_error_pct < (5 : ℝ) ∧
    particle_physics_gap_fill_headline_median_error_pct < (5 : ℝ) ∧
    0 < particle_physics_gap_fill_beats_sota_headlines ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold particle_physics_gap_fill_observable_count; norm_num,
    particle_physics_gap_fill_pooled_median_under_five_pct,
    particle_physics_gap_fill_headline_median_under_five_pct,
    particle_physics_gap_fill_beats_sota_headlines_pos,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
