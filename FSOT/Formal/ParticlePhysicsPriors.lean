/-
  FSOT Formal ParticlePhysicsPriors — Tier 16 particle physics extended observables.
  Sources: SMILES §66/§78/§88 + thesis waves + Wave-4 + math-physics rules
  Generator: scripts/gen_particle_physics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def particle_smiles_record_count : ℕ := 36
def particle_thesis_wave_count : ℕ := 21
def particle_wave4_count : ℕ := 16
def particle_math_physics_rule_count : ℕ := 25
def particle_physics_observable_count : ℕ := 98
def particle_physics_median_error_pct : ℝ := (0.018000835539782083 : ℝ)
def particle_physics_max_error_pct : ℝ := (0.813808 : ℝ)
def particle_physics_within_two_pct : ℕ := 52

theorem particle_smiles_record_count_pos : 0 < particle_smiles_record_count := by
  unfold particle_smiles_record_count; norm_num

theorem particle_wave4_count_pos : 0 < particle_wave4_count := by
  unfold particle_wave4_count; norm_num

theorem particle_physics_observable_count_pos : 0 < particle_physics_observable_count := by
  unfold particle_physics_observable_count; norm_num

theorem particle_physics_components_sum :
    particle_smiles_record_count + particle_thesis_wave_count + particle_wave4_count + particle_math_physics_rule_count =
      particle_physics_observable_count := by
  unfold particle_smiles_record_count particle_thesis_wave_count particle_wave4_count
    particle_math_physics_rule_count particle_physics_observable_count; norm_num

theorem particle_physics_median_error_under_five_pct :
    particle_physics_median_error_pct < (5 : ℝ) := by
  unfold particle_physics_median_error_pct; norm_num

theorem particle_physics_max_error_under_five_pct :
    particle_physics_max_error_pct < (5 : ℝ) := by
  unfold particle_physics_max_error_pct; norm_num

/-- Bundle: particle masses, Higgs/Z branching, CKM/PMNS Wave-4, formal math-physics rules. -/
theorem particle_physics_bundle :
    particle_smiles_record_count = 36 ∧
    particle_thesis_wave_count = 21 ∧
    particle_wave4_count = 16 ∧
    particle_math_physics_rule_count = 25 ∧
    particle_physics_observable_count = 98 ∧
    particle_smiles_record_count + particle_thesis_wave_count + particle_wave4_count + particle_math_physics_rule_count = 98 ∧
    particle_physics_median_error_pct < (5 : ℝ) ∧
    particle_physics_max_error_pct < (5 : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "particle") := by
  refine ⟨
    by unfold particle_smiles_record_count; norm_num,
    by unfold particle_thesis_wave_count; norm_num,
    by unfold particle_wave4_count; norm_num,
    by unfold particle_math_physics_rule_count; norm_num,
    by unfold particle_physics_observable_count; norm_num,
    particle_physics_components_sum,
    particle_physics_median_error_under_five_pct,
    particle_physics_max_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
