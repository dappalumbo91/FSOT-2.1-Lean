/-
  FSOT-native attractor uniqueness — channel dynamics.

  Closed forms match `vendor/fsot_uniqueness_confinement.py` `step_channels`:
    a_color(t)   = a0 · exp(-γ t)
    a_singlet(t) = S_eq + (a0 − S_eq) · exp(-γ_s t)

  This is **not** the classical continuum Yang–Mills path-integral mass-gap
  theorem. That statement stays OPEN_NOT_CLAIMED.
-/

import FSOT.Formal.Scalar
import FSOT.Formal.Bounds
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace FSOT.Formal.UniquenessAttractor

noncomputable section

open Real

/-- Free-color amplitude under linear dampening. -/
def color_amp (a0 γ t : ℝ) : ℝ := a0 * exp (-γ * t)

/-- Color-singlet amplitude relaxing to nuclear `S_eq`. -/
def singlet_amp (a0 seq γ t : ℝ) : ℝ :=
  seq + (a0 - seq) * exp (-γ * t)

/-- Seed-locked free-color damping rate (same stack as Python `free_color_damping_rate`). -/
def gamma_color (sNuc sPart : ℝ) : ℝ :=
  |sNuc| * poof_factor + |sPart| * |suction_factor| +
    |chaos_factor| * acoustic_bleed + psi_con * poof_factor * k

theorem color_amp_at_zero (a0 γ : ℝ) : color_amp a0 γ 0 = a0 := by
  simp [color_amp]

/-- Counterfactual: switch dampening off and free color persists. Load-bearing. -/
theorem color_amp_no_damp (a0 t : ℝ) : color_amp a0 0 t = a0 := by
  simp [color_amp]

theorem color_amp_strictly_damped
    {a0 γ t : ℝ} (ha : 0 < a0) (hγ : 0 < γ) (ht : 0 < t) :
    color_amp a0 γ t < a0 := by
  unfold color_amp
  have hexp : exp (-γ * t) < 1 := by
    rw [exp_lt_one_iff]
    nlinarith
  have hmul : a0 * exp (-γ * t) < a0 * 1 :=
    mul_lt_mul_of_pos_left hexp ha
  simpa using hmul

theorem singlet_amp_at_zero (a0 seq γ : ℝ) : singlet_amp a0 seq γ 0 = a0 := by
  simp [singlet_amp]

theorem singlet_fixed_point (seq γ t : ℝ) : singlet_amp seq seq γ t = seq := by
  simp [singlet_amp]

/-- Counterfactual: γ_s = 0 leaves the singlet where it started. -/
theorem singlet_amp_no_damp (a0 seq t : ℝ) : singlet_amp a0 seq 0 t = a0 := by
  simp [singlet_amp]

/-- Gap to the singlet attractor strictly shrinks when γ_s > 0. -/
theorem singlet_gap_strictly_shrinks
    {a0 seq γ t : ℝ} (hγ : 0 < γ) (ht : 0 < t) (hne : a0 ≠ seq) :
    |singlet_amp a0 seq γ t - seq| < |a0 - seq| := by
  unfold singlet_amp
  have hsimp : seq + (a0 - seq) * exp (-γ * t) - seq = (a0 - seq) * exp (-γ * t) := by
    ring
  rw [hsimp, abs_mul, abs_of_pos (exp_pos _)]
  have hexp : exp (-γ * t) < 1 := by
    rw [exp_lt_one_iff]
    nlinarith
  exact mul_lt_of_lt_one_right (abs_pos.mpr (sub_ne_zero.mpr hne)) hexp

theorem gamma_color_pos (sNuc sPart : ℝ) : 0 < gamma_color sNuc sPart := by
  unfold gamma_color
  have htail : 0 < psi_con * poof_factor * k :=
    mul_pos (mul_pos psi_con_pos poof_factor_pos) k_pos
  have h1 : 0 ≤ |sNuc| * poof_factor :=
    mul_nonneg (abs_nonneg _) (le_of_lt poof_factor_pos)
  have h2 : 0 ≤ |sPart| * |suction_factor| :=
    mul_nonneg (abs_nonneg _) (abs_nonneg _)
  have h3 : 0 ≤ |chaos_factor| * acoustic_bleed :=
    mul_nonneg (abs_nonneg _) (le_of_lt acoustic_bleed_pos)
  linarith [h1, h2, h3, htail]

/-- Free color is not an attractor: γ_color > 0 so a_color(t) damps for t > 0. -/
theorem free_color_not_attractor
    {sNuc sPart a0 t : ℝ} (ha : 0 < a0) (ht : 0 < t) :
    color_amp a0 (gamma_color sNuc sPart) t < a0 :=
  color_amp_strictly_damped ha (gamma_color_pos sNuc sPart) ht

end

end FSOT.Formal.UniquenessAttractor
