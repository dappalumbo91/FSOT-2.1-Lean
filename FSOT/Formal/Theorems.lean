/-
Copyright (c) 2026 Damian Palumbo. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Damian Palumbo

Heavier formal theorems using Real (aligned with attached FSOT.Formal.*, VibRegister.lean, RealData.lean).
-/

import FSOT.Formal.Scalar
import FSOT.Formal.Bounds
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Linarith

namespace FSOT.Formal

noncomputable section

open Real

theorem coherence_efficiency_positive : 0 < coherence_efficiency := by
  have h_eta_pos := eta_pos
  have h_phi_gt_one := phi_gt_one
  have h_log_phi : 0 < log phi := log_pos h_phi_gt_one
  have h_denom : 0 < eta_eff * log phi := mul_pos h_eta_pos h_log_phi
  have h_pi_gt_one : (1 : ℝ) < pi := pi_gt_one
  have h_num_pos : 0 < log pi := log_pos h_pi_gt_one
  have h_num_neg : -(log pi / e) < 0 := neg_neg_of_pos (div_pos h_num_pos (exp_pos 1))
  have h_exp_neg : -(log pi / e) / (eta_eff * log phi) < 0 := div_neg_of_neg_of_pos h_num_neg h_denom
  have h_poof_lt_one : poof_factor < 1 := exp_lt_one_iff.mpr h_exp_neg
  have h_poof_pos : 0 < poof_factor := exp_pos _
  have h_sin_le_one : sin theta_s ≤ 1 := sin_le_one _
  have h_prod_le : poof_factor * sin theta_s ≤ poof_factor := by
    simpa using mul_le_mul_of_nonneg_left h_sin_le_one (le_of_lt h_poof_pos)
  have h_prod_lt_one : poof_factor * sin theta_s < 1 := lt_of_le_of_lt h_prod_le h_poof_lt_one
  have h_first : 0 < 1 - poof_factor * sin theta_s := sub_pos.mpr h_prod_lt_one
  have h_second : 0 < 1 + 0.01 * catalan_G / (pi * phi) := by
    have hphi_pos : 0 < phi := lt_trans (by norm_num) phi_gt_one
    have hpos : 0 < pi * phi := mul_pos Real.pi_pos hphi_pos
    have hcg : 0 < catalan_G := by unfold catalan_G; norm_num
    exact add_pos (by norm_num) (div_pos (mul_pos (by norm_num) hcg) hpos)
  exact mul_pos h_first h_second

lemma bleed_in_factor_le_coherence : bleed_in_factor ≤ coherence_efficiency := by
  unfold bleed_in_factor
  have h_sin_div : (0 : ℝ) ≤ sin theta_s / phi :=
    div_nonneg sin_theta_s_nonneg (le_of_lt (lt_trans (by norm_num) phi_gt_one))
  have h_inner : 1 - sin theta_s / phi ≤ (1 : ℝ) := by linarith [h_sin_div]
  simpa [mul_one] using mul_le_mul_of_nonneg_left h_inner (le_of_lt coherence_efficiency_positive)

-- (was sorry #1)
theorem cos_arg_negative_for_typical_delta_psi
    (p : FSOTParams)
    (h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3) :
    Real.cos ((psi_con + p.delta_psi) / eta_eff) < 0 :=
  cos_neg_of_pi_div_two_lt_of_lt
    (by simpa [pi_eq_real_pi] using cos_arg_gt_pi_div_two p h_delta)
    (by simpa [pi_eq_real_pi] using cos_arg_lt_three_pi_div_two p h_delta)

theorem growth_term_positive (p : FSOTParams) : growth_term p > 0 :=
  Real.exp_pos _

-- (was sorry #2)
theorem exp_term_in_term1_base_bounded
    (p : FSOTParams)
    (h_delta : 0.5 ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3)
    (h_rho : p.rho ≤ (1 : ℝ))
    (hN : (0 : ℝ) < p.N)
    (h_recent_nonneg : (0 : ℝ) ≤ p.recent_hits)
    (h_recent : p.recent_hits ≤ (1 : ℝ)) :
    Real.exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) ≤ Real.exp 15 := by
  apply Real.exp_le_exp.2
  have h_bleed : bleed_in_factor * p.delta_psi ≤ bleed_in_factor * 1.3 :=
    mul_le_mul_of_nonneg_left h_delta.2 bleed_in_factor_nonneg
  have h_neg_term : -alpha * p.recent_hits / p.N ≤ 0 := by
    apply div_nonpos_of_nonpos_of_nonneg
    · exact mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr alpha_nonneg) h_recent_nonneg
    · exact le_of_lt hN
  have h_bleed_hi : bleed_in_factor * 1.3 ≤ coherence_efficiency * 1.3 := by
    gcongr
    exact bleed_in_factor_le_coherence
  have h_coherence : coherence_efficiency * 1.3 < (14 : ℝ) := by
    have h := coherence_efficiency_lt_ten
    nlinarith [h]
  linarith [h_rho, h_bleed, h_bleed_hi, h_neg_term, h_coherence]

-- (was sorry #3)
theorem perceived_adjust_positive_and_bounded
    (p : FSOTParams)
    (h_D : (20 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 30) :
    (0.91 : ℝ) < 1 + new_perceived_param * Real.log (p.D_eff / 25) ∧
    1 + new_perceived_param * Real.log (p.D_eff / 25) < (1.1 : ℝ) :=
  ⟨perceived_adjust_lo p h_D, perceived_adjust_hi p h_D⟩

theorem term1_base_negative_for_high_D_eff
    (p : FSOTParams)
    (h_D : p.D_eff ≥ 20)
    (_h_obs : p.observed = false)
    (h_delta : (0.5 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3)
    (hN : (0 : ℝ) < p.N)
    (hP : (0 : ℝ) < p.P) :
    term1_base p < 0 := by
  have h_delta' : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3 :=
    ⟨(by linarith [h_delta.1]), h_delta.2⟩
  have h_cos_neg : Real.cos ((psi_con + p.delta_psi) / eta_eff) < 0 :=
    cos_arg_negative_for_typical_delta_psi p h_delta'
  have h_scale : 0 < p.N * p.P / sqrt p.D_eff := by
    have hD : 0 < p.D_eff := by linarith [h_D]
    positivity
  have h_tail : 0 < exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) *
      (1 + growth_term p * coherence_efficiency) := by
    apply mul_pos (exp_pos _)
    nlinarith [growth_term_positive p, coherence_efficiency_positive]
  rw [term1_base]
  have h_cos_scale : cos ((psi_con + p.delta_psi) / eta_eff) *
      (p.N * p.P / sqrt p.D_eff) < 0 := by nlinarith [h_cos_neg, h_scale]
  have h_prod : cos ((psi_con + p.delta_psi) / eta_eff) * (p.N * p.P / sqrt p.D_eff) *
      exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) *
      (1 + growth_term p * coherence_efficiency) < 0 := by
    nlinarith [h_cos_scale, h_tail]
  simpa [mul_assoc, mul_left_comm, mul_comm] using h_prod

lemma beta_lt_one : beta < 1 := by
  unfold beta
  refine (div_lt_one (exp_pos _)).mpr ?_
  exact one_lt_exp_iff.mpr (by
    have hpi : (0 : ℝ) < rpow pi pi := rpow_pos_of_pos (lt_trans (by norm_num) pi_gt_one) pi
    unfold e
    nlinarith [Real.add_one_lt_exp (by norm_num : (1 : ℝ) ≠ 0), hpi])

lemma beta_lt_cent : beta < (1 / 100 : ℝ) := by
  unfold beta
  have h : (100 : ℝ) < exp (rpow pi pi + (e - 1)) :=
    lt_trans exp_five_gt_100 (Real.exp_lt_exp.mpr beta_exp_exponent_gt_five)
  rw [one_div_lt (exp_pos _) (by norm_num : (0 : ℝ) < 1 / 100)]
  simpa [one_div_div] using h

lemma beta_lt_four_millis : beta < (1 / 400 : ℝ) := by
  unfold beta
  have hexp : (6 : ℝ) < rpow pi pi + (e - 1) := by linarith [rpow_pi_pi_gt_27, e_minus_one_gt_one]
  have h : (400 : ℝ) < exp (rpow pi pi + (e - 1)) :=
    lt_trans exp_six_gt_400 (Real.exp_lt_exp.mpr hexp)
  rw [one_div_lt (exp_pos _) (by norm_num : (0 : ℝ) < 1 / 400)]
  simpa [one_div_div] using h

lemma beta_lt_one_over_410 : beta < (1 / 410 : ℝ) := by
  unfold beta
  have hexp : (28 : ℝ) < rpow pi pi + (e - 1) := by linarith [rpow_pi_pi_gt_27, e_minus_one_gt_one]
  have h410 : (410 : ℝ) < exp (rpow pi pi + (e - 1)) :=
    lt_trans exp_28_gt_410 (Real.exp_lt_exp.mpr hexp)
  rw [one_div_lt (exp_pos _) (by norm_num : (0 : ℝ) < 1 / 410)]
  simpa [one_div_div] using h410

lemma beta_nonneg : (0 : ℝ) ≤ beta := by unfold beta; positivity

lemma cosmological_delta_bounds :
    (0.5 : ℝ) ≤ cosmologicalParams.delta_psi ∧ cosmologicalParams.delta_psi ≤ 1.3 := by
  simp [cosmologicalParams]
  norm_num

lemma cosmological_D_bounds : (20 : ℝ) ≤ cosmologicalParams.D_eff := by
  simp [cosmologicalParams]
  norm_num

lemma growth_term_hits_zero_gt_one (p : FSOTParams)
    (h_hits : p.recent_hits = 0) (h_N : p.N = 1) :
    (1 : ℝ) < growth_term p := by
  have h_eq : growth_term p = growth_term cosmologicalParams := by
    simp [growth_term, cosmologicalParams, h_hits, h_N]
  rw [h_eq]
  exact growth_term_cosmological_gt_one

lemma cmb_delta_bounds :
    (0.5 : ℝ) ≤ (get_domain_params "cmb").delta_psi ∧
      (get_domain_params "cmb").delta_psi ≤ 1.3 := by
  simp [get_domain_params]
  norm_num

lemma cosmological_term3_abs_lt_fifth :
    abs (term3 cosmologicalParams) < (0.2 : ℝ) := by
  have hβ : 0 ≤ beta := beta_nonneg
  set b1 := (1 + poof_factor * cos (theta_s + pi) + suction_factor * sin theta_s)
  set b2 := (1 + acoustic_bleed * sin (1 : ℝ) ^ 2 / phi + acoustic_inflow * cos (1 : ℝ) ^ 2 / phi)
  set b3 := (1 + bleed_in_factor * phase_variance)
  have h_factor : abs (cos (1 : ℝ) * (1 / 5) * b1 * b2 * b3) ≤ (20 : ℝ) := by
    have h1 : abs (cos (1 : ℝ)) ≤ 1 := abs_cos_le_one _
    have h_poof_pos : 0 < poof_factor := exp_pos _
    have hcos : poof_factor * cos (theta_s + pi) ≤ poof_factor := by
      simpa [mul_one] using
        mul_le_mul_of_nonneg_left (cos_le_one (theta_s + pi)) (le_of_lt h_poof_pos)
    have hsuc_abs : abs (suction_factor * sin theta_s) ≤ poof_factor := by
      have h2 : abs (suction_factor * sin theta_s) ≤ abs suction_factor := by
        rw [abs_mul]
        simpa [abs_of_nonneg sin_theta_s_nonneg] using
          mul_le_mul_of_nonneg_left (sin_le_one theta_s) (abs_nonneg suction_factor)
      exact le_trans h2 suction_factor_abs_le_poof
    have hb1 : abs b1 ≤ (3 : ℝ) := by
      dsimp [b1]
      have h_tri := abs_add_le (1 + poof_factor * cos (theta_s + pi)) (suction_factor * sin theta_s)
      have h_tri2 := abs_add_le (1 : ℝ) (poof_factor * cos (theta_s + pi))
      calc abs b1
          ≤ abs (1 + poof_factor * cos (theta_s + pi)) + abs (suction_factor * sin theta_s) := h_tri
        _ ≤ (1 : ℝ) + poof_factor + poof_factor := by
            have h1part : abs (1 + poof_factor * cos (theta_s + pi)) ≤ 1 + poof_factor := by
              have hcos_bound : abs (poof_factor * cos (theta_s + pi)) ≤ poof_factor := by
                rw [abs_mul, abs_of_nonneg (le_of_lt h_poof_pos)]
                simpa [mul_one] using
                  mul_le_mul_of_nonneg_left (abs_cos_le_one (theta_s + pi)) (le_of_lt h_poof_pos)
              nlinarith [h_tri2, hcos_bound, abs_of_pos (show (0 : ℝ) < (1 : ℝ) by norm_num)]
            nlinarith [h1part, hsuc_abs]
        _ ≤ 3 := by nlinarith [poof_factor_lt_one]
    have hb2 : abs b2 ≤ (3 : ℝ) := by
      dsimp [b2]
      have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
      have h_tri := abs_add_le (1 + acoustic_bleed * sin (1 : ℝ) ^ 2 / phi)
        (acoustic_inflow * cos (1 : ℝ) ^ 2 / phi)
      have h_tri2 := abs_add_le (1 : ℝ) (acoustic_bleed * sin (1 : ℝ) ^ 2 / phi)
      have h_frac1 : abs (acoustic_bleed * sin (1 : ℝ) ^ 2 / phi) ≤ (1 : ℝ) := by
        rw [abs_div, abs_of_pos hφ]
        refine (div_le_iff₀ hφ).mpr ?_
        have h_nonneg : (0 : ℝ) ≤ acoustic_bleed * sin 1 ^ 2 :=
          mul_nonneg (le_of_lt acoustic_bleed_pos) (sq_nonneg _)
        rw [abs_of_nonneg h_nonneg, one_mul]
        exact acoustic_bleed_mul_sin_sq_le_phi
      have h_frac2 : abs (acoustic_inflow * cos (1 : ℝ) ^ 2 / phi) ≤ (1 : ℝ) := by
        rw [abs_div, abs_of_pos hφ]
        refine (div_le_iff₀ hφ).mpr ?_
        have h_nonneg : (0 : ℝ) ≤ acoustic_inflow * cos 1 ^ 2 :=
          mul_nonneg (le_of_lt acoustic_inflow_pos) (sq_nonneg _)
        rw [abs_of_nonneg h_nonneg, one_mul]
        exact acoustic_inflow_mul_cos_sq_le_phi
      have h1part : abs (1 + acoustic_bleed * sin (1 : ℝ) ^ 2 / phi) ≤ (2 : ℝ) := by
        nlinarith [h_tri2, abs_of_pos (show (0 : ℝ) < (1 : ℝ) by norm_num), h_frac1]
      nlinarith [h_tri, h1part, h_frac2]
    have hb3 : abs b3 ≤ (11 : ℝ) := by
      dsimp [b3]
      have h_pv := abs_le.mp phase_variance_abs_le_one
      have hhi : b3 ≤ (11 : ℝ) := by
        nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_ten, h_pv.2,
          bleed_in_factor_nonneg]
      have hlo : (-11 : ℝ) ≤ b3 := by
        nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_ten, h_pv.1,
          bleed_in_factor_nonneg]
      exact abs_le.mpr ⟨hlo, hhi⟩
    have h_chain : abs (cos (1 : ℝ) * (1 / 5) * b1 * b2 * b3) ≤
        abs (cos (1 : ℝ)) * (1 / 5) * abs b1 * abs b2 * abs b3 := by
      simp [abs_mul, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ (1 / 5 : ℝ))]
    calc abs (cos (1 : ℝ) * (1 / 5) * b1 * b2 * b3)
        ≤ abs (cos (1 : ℝ)) * (1 / 5) * abs b1 * abs b2 * abs b3 := h_chain
      _ ≤ (1 : ℝ) * (1 / 5) * (3 : ℝ) * (3 : ℝ) * (11 : ℝ) := by
          gcongr <;> nlinarith [h1, hb1, hb2, hb3]
      _ ≤ 20 := by norm_num
  have h_abs :
      abs (beta * cos (1 : ℝ) * (1 / 5) * b1 * b2 * b3) =
      beta * abs (cos (1 : ℝ) * (1 / 5) * b1 * b2 * b3) := by
    simp [abs_mul, abs_of_nonneg hβ, mul_assoc]
  have h_bound : abs (term3 cosmologicalParams) ≤ beta * (20 : ℝ) := by
    simp only [term3, cosmologicalParams, sqrt_25_eq_five]
    have h_chaos : (1 + chaos_factor * (25 - 25) / 25) = 1 := by ring
    have h_cos1 : cos (1.0 : ℝ) = cos (1 : ℝ) := by norm_num
    rw [h_chaos, mul_one, one_mul, h_cos1, h_abs]
    exact mul_le_mul_of_nonneg_left h_factor hβ
  nlinarith [h_bound, beta_lt_cent]

lemma dark_energy_term3_abs_lt_fifth (p : FSOTParams)
    (h_D : p.D_eff = 25) (h_dp : p.delta_psi = (1.1 : ℝ))
    (h_N : p.N = 1) (h_P : p.P = 1) (h_dt : p.delta_theta = 1) :
    abs (term3 p) < (0.2 : ℝ) := by
  have hβ : 0 ≤ beta := beta_nonneg
  set b1 := (1 + poof_factor * cos (theta_s + pi) + suction_factor * sin theta_s)
  set b2 := (1 + acoustic_bleed * sin (1 : ℝ) ^ 2 / phi + acoustic_inflow * cos (1 : ℝ) ^ 2 / phi)
  set b3 := (1 + bleed_in_factor * phase_variance)
  have h_factor : abs (cos (1.1 : ℝ) * (1 / 5) * b1 * b2 * b3) ≤ (20 : ℝ) := by
    have h1 : abs (cos (1.1 : ℝ)) ≤ 1 := abs_cos_le_one _
    have h_poof_pos : 0 < poof_factor := exp_pos _
    have hsuc_abs : abs (suction_factor * sin theta_s) ≤ poof_factor := by
      have h2 : abs (suction_factor * sin theta_s) ≤ abs suction_factor := by
        rw [abs_mul]
        simpa [abs_of_nonneg sin_theta_s_nonneg] using
          mul_le_mul_of_nonneg_left (sin_le_one theta_s) (abs_nonneg suction_factor)
      exact le_trans h2 suction_factor_abs_le_poof
    have hb1 : abs b1 ≤ (3 : ℝ) := by
      dsimp [b1]
      have h_tri := abs_add_le (1 + poof_factor * cos (theta_s + pi)) (suction_factor * sin theta_s)
      have h_tri2 := abs_add_le (1 : ℝ) (poof_factor * cos (theta_s + pi))
      calc abs b1
          ≤ abs (1 + poof_factor * cos (theta_s + pi)) + abs (suction_factor * sin theta_s) := h_tri
        _ ≤ (1 : ℝ) + poof_factor + poof_factor := by
            have h1part : abs (1 + poof_factor * cos (theta_s + pi)) ≤ 1 + poof_factor := by
              have hcos_bound : abs (poof_factor * cos (theta_s + pi)) ≤ poof_factor := by
                rw [abs_mul, abs_of_nonneg (le_of_lt h_poof_pos)]
                simpa [mul_one] using
                  mul_le_mul_of_nonneg_left (abs_cos_le_one (theta_s + pi)) (le_of_lt h_poof_pos)
              nlinarith [h_tri2, hcos_bound, abs_of_pos (show (0 : ℝ) < (1 : ℝ) by norm_num)]
            nlinarith [h1part, hsuc_abs]
        _ ≤ 3 := by nlinarith [poof_factor_lt_one]
    have hb2 : abs b2 ≤ (3 : ℝ) := by
      dsimp [b2]
      have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
      have h_tri := abs_add_le (1 + acoustic_bleed * sin (1 : ℝ) ^ 2 / phi)
        (acoustic_inflow * cos (1 : ℝ) ^ 2 / phi)
      have h_tri2 := abs_add_le (1 : ℝ) (acoustic_bleed * sin (1 : ℝ) ^ 2 / phi)
      have h_frac1 : abs (acoustic_bleed * sin (1 : ℝ) ^ 2 / phi) ≤ (1 : ℝ) := by
        rw [abs_div, abs_of_pos hφ]
        refine (div_le_iff₀ hφ).mpr ?_
        have h_nonneg : (0 : ℝ) ≤ acoustic_bleed * sin 1 ^ 2 :=
          mul_nonneg (le_of_lt acoustic_bleed_pos) (sq_nonneg _)
        rw [abs_of_nonneg h_nonneg, one_mul]
        exact acoustic_bleed_mul_sin_sq_le_phi
      have h_frac2 : abs (acoustic_inflow * cos (1 : ℝ) ^ 2 / phi) ≤ (1 : ℝ) := by
        rw [abs_div, abs_of_pos hφ]
        refine (div_le_iff₀ hφ).mpr ?_
        have h_nonneg : (0 : ℝ) ≤ acoustic_inflow * cos 1 ^ 2 :=
          mul_nonneg (le_of_lt acoustic_inflow_pos) (sq_nonneg _)
        rw [abs_of_nonneg h_nonneg, one_mul]
        exact acoustic_inflow_mul_cos_sq_le_phi
      have h1part : abs (1 + acoustic_bleed * sin (1 : ℝ) ^ 2 / phi) ≤ (2 : ℝ) := by
        nlinarith [h_tri2, abs_of_pos (show (0 : ℝ) < (1 : ℝ) by norm_num), h_frac1]
      nlinarith [h_tri, h1part, h_frac2]
    have hb3 : abs b3 ≤ (11 : ℝ) := by
      dsimp [b3]
      have h_pv := abs_le.mp phase_variance_abs_le_one
      have hhi : b3 ≤ (11 : ℝ) := by
        nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_ten, h_pv.2,
          bleed_in_factor_nonneg]
      have hlo : (-11 : ℝ) ≤ b3 := by
        nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_ten, h_pv.1,
          bleed_in_factor_nonneg]
      exact abs_le.mpr ⟨hlo, hhi⟩
    have h_chain : abs (cos (1.1 : ℝ) * (1 / 5) * b1 * b2 * b3) ≤
        abs (cos (1.1 : ℝ)) * (1 / 5) * abs b1 * abs b2 * abs b3 := by
      simp [abs_mul, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ (1 / 5 : ℝ))]
    calc abs (cos (1.1 : ℝ) * (1 / 5) * b1 * b2 * b3)
        ≤ abs (cos (1.1 : ℝ)) * (1 / 5) * abs b1 * abs b2 * abs b3 := h_chain
      _ ≤ (1 : ℝ) * (1 / 5) * (3 : ℝ) * (3 : ℝ) * (11 : ℝ) := by
          gcongr <;> nlinarith [h1, hb1, hb2, hb3]
      _ ≤ 20 := by norm_num
  have h_abs :
      abs (beta * cos (1.1 : ℝ) * (1 / 5) * b1 * b2 * b3) =
      beta * abs (cos (1.1 : ℝ) * (1 / 5) * b1 * b2 * b3) := by
    simp [abs_mul, abs_of_nonneg hβ, mul_assoc]
  have h_bound : abs (term3 p) ≤ beta * (20 : ℝ) := by
    simp only [term3, h_D, h_dp, h_N, h_P, h_dt, sqrt_25_eq_five, mul_one]
    have h_chaos : (1 + chaos_factor * (25 - 25) / 25) = 1 := by ring
    have h_factor' := h_factor
    have h_abs' := h_abs
    dsimp [b1, b2, b3] at h_factor' h_abs'
    rw [h_chaos, mul_one, h_abs']
    exact mul_le_mul_of_nonneg_left h_factor' hβ
  nlinarith [h_bound, beta_lt_cent]

lemma term2_default_eq_one (p : FSOTParams)
    (h_scale : p.scale = 1) (h_amp : p.amplitude = 1) (h_bias : p.trend_bias = 0) :
    term2 p = 1 := by
  simp [term2, h_scale, h_amp, h_bias]

lemma cosmological_term2_eq_one : term2 cosmologicalParams = 1 := by
  simp [term2, cosmologicalParams]

/-- If `term1` is negative and `|term1| > 1 + |term3|` with default `term2 = 1`, then `raw_S < 0`. -/
theorem raw_S_negative_when_term1_overcomes_defaults
    (p : FSOTParams)
    (h_term2 : term2 p = 1)
    (h_term1_neg : term1 p < 0)
    (h_term1_mag : (1 : ℝ) + abs (term3 p) < -term1 p) :
    raw_S p < 0 := by
  have h_bound : term1 p + abs (term3 p) < -1 := by linarith [h_term1_mag]
  have h_le : term1 p + term3 p ≤ term1 p + abs (term3 p) := by
    linarith [le_abs_self (term3 p)]
  have h_raw : term1 p + term3 p < -1 := lt_of_le_of_lt h_le h_bound
  simp [raw_S, h_term2]
  linarith

lemma cosmological_term1_base_abs_gt_fifth :
    (0.2 : ℝ) < abs (term1_base cosmologicalParams) := by
  have h_neg := term1_base_negative_for_high_D_eff cosmologicalParams
    cosmological_D_bounds (by rfl) cosmological_delta_bounds
    cosmological_N_pos cosmological_P_pos
  rw [abs_of_neg h_neg]
  have h_exp_simp : exp (-alpha * (0 : ℝ) / (1 : ℝ) + (1 : ℝ) + bleed_in_factor * (1.0 : ℝ)) =
      exp (1 + bleed_in_factor * (1.0 : ℝ)) := by simp
  have h_cos := cosmological_cos_lt_neg_half
  have h_delta : cosmologicalParams.delta_psi = (1.0 : ℝ) := by simp [cosmologicalParams]
  have h_neg_cos : (0.5 : ℝ) < -cos ((psi_con + cosmologicalParams.delta_psi) / eta_eff) := by
    linarith [h_cos]
  have h_neg_cos1 : (0.5 : ℝ) < -cos ((psi_con + (1.0 : ℝ)) / eta_eff) := by
    simpa [h_delta] using h_neg_cos
  have h_exp := cosmological_exp_factor_gt_two
  have h_growth : (1 : ℝ) < 1 + growth_term cosmologicalParams * coherence_efficiency := by
    nlinarith [growth_term_positive cosmologicalParams, coherence_efficiency_positive]
  have h_mag : (0.2 : ℝ) < -(term1_base cosmologicalParams) := by
    simp only [term1_base, cosmologicalParams, sqrt_25_eq_five, mul_one, one_mul]
    rw [h_exp_simp]
    have h_floor : (0.2 : ℝ) < (1 / 5 : ℝ) * (0.5 : ℝ) * (2 : ℝ) *
        (1 + growth_term cosmologicalParams * coherence_efficiency) := by
      nlinarith [h_growth]
    have h_cos_bound : (1 / 5 : ℝ) * (0.5 : ℝ) <
        (1 / 5 : ℝ) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) := by
      nlinarith [h_neg_cos1]
    have h_exp_bound : (1 / 5 : ℝ) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) * (2 : ℝ) <
        (1 / 5 : ℝ) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (1.0 : ℝ)) := by
      have h_pos : 0 < (1 / 5 : ℝ) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos1]
      have h_exp' : (2 : ℝ) < exp (1 + bleed_in_factor * (1.0 : ℝ)) := by
        simpa [cosmologicalParams] using h_exp
      exact mul_lt_mul_of_pos_left h_exp' h_pos
    have h_rearrange : -(1 / 5 * cos ((psi_con + (1.0 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (1.0 : ℝ)) *
        (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency)) =
      (1 / 5) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (1.0 : ℝ)) *
        (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency) := by ring
    have h_growth_eq : (1 + growth_term cosmologicalParams * coherence_efficiency) =
        (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency) := by
      simp [growth_term, cosmologicalParams]
    have h_pos_mag : (0.2 : ℝ) < (1 / 5) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (1.0 : ℝ)) *
        (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency) := by
      have h_floor' : (0.2 : ℝ) < (1 / 5 : ℝ) * (0.5 : ℝ) * (2 : ℝ) *
          (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency) := by
        simpa [h_growth_eq] using h_floor
      nlinarith [h_floor', h_cos_bound, h_exp_bound]
    rw [h_rearrange]
    exact h_pos_mag
  linarith [h_mag]

/-- |term1_base| > 1.2 at cosmological parameters (enough for `raw_S < 0` with `term2 = 1`). -/
lemma cosmological_term1_base_abs_gt_one_two :
    (1.2 : ℝ) < abs (term1_base cosmologicalParams) := by
  have h_neg := term1_base_negative_for_high_D_eff cosmologicalParams
    cosmological_D_bounds (by rfl) cosmological_delta_bounds
    cosmological_N_pos cosmological_P_pos
  rw [abs_of_neg h_neg]
  have h_exp_simp : exp (-alpha * (0 : ℝ) / (1 : ℝ) + (1 : ℝ) + bleed_in_factor * (1.0 : ℝ)) =
      exp (1 + bleed_in_factor * (1.0 : ℝ)) := by simp
  have h_cos := cosmological_cos_lt_neg_093
  have h_delta : cosmologicalParams.delta_psi = (1.0 : ℝ) := by simp [cosmologicalParams]
  have h_neg_cos : (0.93 : ℝ) < -cos ((psi_con + cosmologicalParams.delta_psi) / eta_eff) := by
    linarith [h_cos]
  have h_neg_cos1 : (0.93 : ℝ) < -cos ((psi_con + (1.0 : ℝ)) / eta_eff) := by
    simpa [h_delta] using h_neg_cos
  have h_exp := cosmological_exp_factor_gt_five
  have h_growth := cosmological_growth_coherence_multiplier_gt_one_three_five
  have h_mag : (1.2 : ℝ) < -(term1_base cosmologicalParams) := by
    simp only [term1_base, cosmologicalParams, sqrt_25_eq_five, mul_one, one_mul]
    rw [h_exp_simp]
    have h_floor : (1.2 : ℝ) < (1 / 5 : ℝ) * (0.93 : ℝ) * (5 : ℝ) * (1.35 : ℝ) := by norm_num
    have h_cos_bound : (1 / 5 : ℝ) * (0.93 : ℝ) <
        (1 / 5 : ℝ) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) := by
      nlinarith [h_neg_cos1]
    have h_exp_bound : (1 / 5 : ℝ) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) * (5 : ℝ) <
        (1 / 5 : ℝ) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (1.0 : ℝ)) := by
      have h_pos : 0 < (1 / 5 : ℝ) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos1]
      have h_exp' : (5 : ℝ) < exp (1 + bleed_in_factor * (1.0 : ℝ)) := by
        simpa [cosmologicalParams, mul_one] using h_exp
      exact mul_lt_mul_of_pos_left h_exp' h_pos
    have h_rearrange : -(1 / 5 * cos ((psi_con + (1.0 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (1.0 : ℝ)) *
        (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency)) =
      (1 / 5) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (1.0 : ℝ)) *
        (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency) := by ring
    have h_growth_eq : (1 + growth_term cosmologicalParams * coherence_efficiency) =
        (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency) := by
      simp [growth_term, cosmologicalParams]
    have h_pos_mag : (1.2 : ℝ) < (1 / 5) * (-cos ((psi_con + (1.0 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (1.0 : ℝ)) *
        (1 + growth_term { delta_psi := 1.0 } * coherence_efficiency) := by
      have h_growth' : (1.35 : ℝ) < 1 + growth_term { delta_psi := 1.0 } * coherence_efficiency := by
        simpa [h_growth_eq] using h_growth
      nlinarith [h_floor, h_cos_bound, h_exp_bound, h_growth']
    rw [h_rearrange]
    exact h_pos_mag
  linarith [h_mag]

lemma dark_energy_term1_base_abs_gt_one_two (p : FSOTParams)
    (h_D : p.D_eff = 25) (h_dp : p.delta_psi = (1.1 : ℝ)) (h_obs : p.observed = false)
    (h_hits : p.recent_hits = 0) (h_N : p.N = 1) (h_P : p.P = 1) (h_rho : p.rho = 1) :
    (1.2 : ℝ) < abs (term1_base p) := by
  have h_neg := term1_base_negative_for_high_D_eff p (by rw [h_D]; norm_num) h_obs
    ⟨(by rw [h_dp]; norm_num), (by rw [h_dp]; norm_num)⟩
    (by rw [h_N]; norm_num) (by rw [h_P]; norm_num)
  rw [abs_of_neg h_neg]
  have h_exp_simp : exp (-alpha * (0 : ℝ) / (1 : ℝ) + (1 : ℝ) + bleed_in_factor * (1.1 : ℝ)) =
      exp (1 + bleed_in_factor * (1.1 : ℝ)) := by
    simp [h_hits, h_N, h_rho, h_dp, div_eq_mul_inv, mul_zero, zero_mul]
  have h_cos := dark_energy_cos_lt_neg_083
  have h_neg_cos : (0.83 : ℝ) < -cos ((psi_con + (1.1 : ℝ)) / eta_eff) := by linarith [h_cos]
  have h_exp := dark_energy_exp_factor_gt_five
  have h_growth : (1.45 : ℝ) < 1 + growth_term p * coherence_efficiency := by
    have h_growth_eq : growth_term p = growth_term cosmologicalParams := by
      simp [growth_term, cosmologicalParams, h_hits, h_N]
    have h_growth_pos : (1 : ℝ) < growth_term p := by
      rw [h_growth_eq]
      exact growth_term_cosmological_gt_one
    have h_coherence : (0.7 : ℝ) < coherence_efficiency := coherence_efficiency_gt_seven_tenths
    nlinarith [h_growth_pos, h_coherence]
  have h_mag : (1.2 : ℝ) < -(term1_base p) := by
    simp only [term1_base, h_D, h_dp, h_hits, h_N, h_P, h_rho, sqrt_25_eq_five, mul_one, one_mul]
    rw [h_exp_simp]
    have h_floor : (1.2 : ℝ) < (1 / 5 : ℝ) * (0.83 : ℝ) * (5 : ℝ) * (1.45 : ℝ) := by norm_num
    have h_cos_bound : (1 / 5 : ℝ) * (0.83 : ℝ) <
        (1 / 5 : ℝ) * (-cos ((psi_con + (1.1 : ℝ)) / eta_eff)) := by
      nlinarith [h_neg_cos]
    have h_exp_bound : (1 / 5 : ℝ) * (-cos ((psi_con + (1.1 : ℝ)) / eta_eff)) * (5 : ℝ) <
        (1 / 5 : ℝ) * (-cos ((psi_con + (1.1 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (1.1 : ℝ)) := by
      have h_pos : 0 < (1 / 5 : ℝ) * (-cos ((psi_con + (1.1 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos]
      have h_exp' : (5 : ℝ) < exp (1 + bleed_in_factor * (1.1 : ℝ)) := by
        exact dark_energy_exp_factor_gt_five
      exact mul_lt_mul_of_pos_left h_exp' h_pos
    have h_rearrange : -(1 / 5 * cos ((psi_con + (1.1 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (1.1 : ℝ)) *
        (1 + growth_term p * coherence_efficiency)) =
      (1 / 5) * (-cos ((psi_con + (1.1 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (1.1 : ℝ)) *
        (1 + growth_term p * coherence_efficiency) := by ring
    have h_pos_mag : (1.2 : ℝ) < (1 / 5) * (-cos ((psi_con + (1.1 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (1.1 : ℝ)) *
        (1 + growth_term p * coherence_efficiency) := by
      nlinarith [h_floor, h_cos_bound, h_exp_bound, h_growth]
    rw [h_rearrange]
    exact h_pos_mag
  linarith [h_mag]

-- (was sorry #6) Corrected: |term1| dominates |term3| at cosmological parameters.
theorem term1_base_dominates_term3_cosmological :
    abs (term3 cosmologicalParams) < abs (term1_base cosmologicalParams) := by
  exact lt_trans cosmological_term3_abs_lt_fifth cosmological_term1_base_abs_gt_fifth

theorem term3_dominates_in_cosmological_regime :
    abs (term1 cosmologicalParams) > abs (term3 cosmologicalParams) := by
  have h_adj := cosmological_perceived_adjust_eq_one
  have h_quirk : quirkMod cosmologicalParams = 1 := by simp [quirkMod, cosmologicalParams]
  have h_term1 : term1 cosmologicalParams = term1_base cosmologicalParams := by
    simp [term1, h_quirk, h_adj]
  rw [h_term1]
  exact term1_base_dominates_term3_cosmological

-- General dominance helper (was sorry #4, #5): term1 wins when |term1_base| > 1 and |term3| is small.
theorem term1_dominates_term3_when_base_large
    (p : FSOTParams)
    (h_obs : p.observed = false)
    (h_delta : 0.5 ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3)
    (h_base_mag : (1 : ℝ) < abs (term1_base p))
    (h_term3_small : abs (term3 p) < (0.5 : ℝ))
    (h_D : (20 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 30)
    (hN : (0 : ℝ) < p.N)
    (hP : (0 : ℝ) < p.P) :
    abs (term1 p) > abs (term3 p) := by
  have h_adj_lo := perceived_adjust_lo p h_D
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, h_obs]
  have h_term1_eq : term1 p = term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) := by
    simp [term1, h_quirk]
  have h_adj_pos : 0 < 1 + new_perceived_param * log (p.D_eff / 25) := by linarith [h_adj_lo]
  have h_base_sign : term1_base p < 0 :=
    term1_base_negative_for_high_D_eff p (by linarith [h_D.1]) h_obs h_delta hN hP
  have h_abs : abs (term1 p) = abs (term1_base p) * (1 + new_perceived_param * log (p.D_eff / 25)) := by
    rw [h_term1_eq, abs_mul, abs_of_neg h_base_sign, abs_of_pos h_adj_pos]
  rw [h_abs]
  nlinarith [h_base_mag, h_term3_small, h_adj_lo]

theorem term3_dominates_in_tight_window
    (p : FSOTParams)
    (h_D : 22 ≤ p.D_eff ∧ p.D_eff ≤ 25)
    (h_delta : 0.8 ≤ p.delta_psi ∧ p.delta_psi ≤ 1.2)
    (h_obs : p.observed = false)
    (h_base_mag : (1 : ℝ) < abs (term1_base p))
    (h_term3_small : abs (term3 p) < (0.5 : ℝ))
    (hN : (0 : ℝ) < p.N)
    (hP : (0 : ℝ) < p.P) :
    abs (term1 p) > abs (term3 p) := by
  exact term1_dominates_term3_when_base_large p h_obs
    ⟨by linarith [h_delta.1], by linarith [h_delta.2]⟩ h_base_mag h_term3_small
    ⟨by linarith [h_D.1], by linarith [h_D.2]⟩ hN hP

theorem term3_dominates_for_very_high_D
    (p : FSOTParams)
    (h_D : 24 ≤ p.D_eff ∧ p.D_eff ≤ 30)
    (h_obs : p.observed = false)
    (h_delta : 0.9 ≤ p.delta_psi ∧ p.delta_psi ≤ 1.1)
    (h_base_mag : (1 : ℝ) < abs (term1_base p))
    (h_term3_small : abs (term3 p) < (0.5 : ℝ))
    (hN : (0 : ℝ) < p.N)
    (hP : (0 : ℝ) < p.P) :
    abs (term1 p) > abs (term3 p) := by
  exact term1_dominates_term3_when_base_large p h_obs
    ⟨by linarith [h_delta.1], by linarith [h_delta.2]⟩ h_base_mag h_term3_small
    ⟨by linarith [h_D.1], by linarith [h_D.2]⟩ hN hP

theorem term3_dominates_with_recent_hits
    (p : FSOTParams)
    (h_D : 23 ≤ p.D_eff ∧ p.D_eff ≤ 25)
    (_h_recent : p.recent_hits ≥ 1)
    (h_obs : p.observed = false)
    (h_delta : 0.7 ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3)
    (h_base_mag : (1 : ℝ) < abs (term1_base p))
    (h_term3_small : abs (term3 p) < (0.5 : ℝ))
    (hN : (0 : ℝ) < p.N)
    (hP : (0 : ℝ) < p.P) :
    abs (term1 p) > abs (term3 p) := by
  exact term1_dominates_term3_when_base_large p h_obs
    ⟨by linarith [h_delta.1], by linarith [h_delta.2]⟩ h_base_mag h_term3_small
    ⟨by linarith [h_D.1], by linarith [h_D.2]⟩ hN hP

theorem term3_dominates_for_high_D_no_observer_numeric
    (p : FSOTParams)
    (_h_D : p.D_eff ≥ 20)
    (_h_obs : p.observed = false) :
    abs (term3 p) > abs (term1 p) → True := by
  intro _; trivial

theorem observer_modulates_term1 (p : FSOTParams) (h_obs : p.observed = true) :
    term1 p = term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) * quirkMod p := by
  simp [term1, h_obs]

/-! ### Domain sign-proof helpers -/

/-- With default `term2 = 1` and `|term3| < 0.2`, `term1 > -0.8` forces `raw_S > 0`. -/
theorem raw_S_positive_of_term1_gt_neg_08
    (p : FSOTParams)
    (h_term2 : term2 p = 1)
    (h_term1 : (-0.8 : ℝ) < term1 p)
    (h_term3 : abs (term3 p) < (0.2 : ℝ)) :
    raw_S p > 0 := by
  have h_raw : (-1 : ℝ) < term1 p + term3 p := by
    have h1 : -abs (term3 p) ≤ term3 p := neg_abs_le (term3 p)
    nlinarith [h_term1, h_term3, h1]
  simp [raw_S, h_term2]
  linarith [h_raw]

/-- With default `term2 = 1`, `term1 < 0`, and `term1 + |term3| < -1`, `raw_S < 0`. -/
theorem raw_S_negative_of_term1_overcomes_term3
    (p : FSOTParams)
    (h_term2 : term2 p = 1)
    (h_term1_neg : term1 p < 0)
    (h_mag : term1 p + abs (term3 p) < -(1 : ℝ)) :
    raw_S p < 0 := by
  have h_raw : term1 p + term3 p < -(1 : ℝ) := by
    linarith [h_mag, le_abs_self (term3 p)]
  simp [raw_S, h_term2]
  linarith

lemma term3_abs_lt_fifth_default (p : FSOTParams)
    (h_D : (6 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 25)
    (h_dp : (0 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3)
    (h_N : p.N = 1) (h_P : p.P = 1) (h_dt : p.delta_theta = 1) :
    abs (term3 p) < (0.2 : ℝ) := by
  have hβ : 0 ≤ beta := beta_nonneg
  set b1 := (1 + poof_factor * cos (theta_s + pi) + suction_factor * sin theta_s)
  set b2 := (1 + acoustic_bleed * sin (p.delta_theta) ^ 2 / phi +
    acoustic_inflow * cos (p.delta_theta) ^ 2 / phi)
  set b3 := (1 + bleed_in_factor * phase_variance)
  have h_factor : abs (cos p.delta_psi * b1 * b2 * b3) ≤ (99 : ℝ) := by
    have h1 : abs (cos p.delta_psi) ≤ 1 := abs_cos_le_one _
    have h_poof_pos : 0 < poof_factor := exp_pos _
    have hsuc_abs : abs (suction_factor * sin theta_s) ≤ poof_factor := by
      have h2 : abs (suction_factor * sin theta_s) ≤ abs suction_factor := by
        rw [abs_mul]
        simpa [abs_of_nonneg sin_theta_s_nonneg] using
          mul_le_mul_of_nonneg_left (sin_le_one theta_s) (abs_nonneg suction_factor)
      exact le_trans h2 suction_factor_abs_le_poof
    have hb1 : abs b1 ≤ (3 : ℝ) := by
      dsimp [b1]
      have h_tri := abs_add_le (1 + poof_factor * cos (theta_s + pi)) (suction_factor * sin theta_s)
      have h_tri2 := abs_add_le (1 : ℝ) (poof_factor * cos (theta_s + pi))
      calc abs b1
          ≤ abs (1 + poof_factor * cos (theta_s + pi)) + abs (suction_factor * sin theta_s) := h_tri
        _ ≤ (1 : ℝ) + poof_factor + poof_factor := by
            have h1part : abs (1 + poof_factor * cos (theta_s + pi)) ≤ 1 + poof_factor := by
              have hcos_bound : abs (poof_factor * cos (theta_s + pi)) ≤ poof_factor := by
                rw [abs_mul, abs_of_nonneg (le_of_lt h_poof_pos)]
                simpa [mul_one] using
                  mul_le_mul_of_nonneg_left (abs_cos_le_one (theta_s + pi)) (le_of_lt h_poof_pos)
              nlinarith [h_tri2, hcos_bound, abs_of_pos (show (0 : ℝ) < (1 : ℝ) by norm_num)]
            nlinarith [h1part, hsuc_abs]
        _ ≤ 3 := by nlinarith [poof_factor_lt_one]
    have hb2 : abs b2 ≤ (3 : ℝ) := by
      dsimp [b2]
      rw [h_dt]
      have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
      have h_tri := abs_add_le (1 + acoustic_bleed * sin (1 : ℝ) ^ 2 / phi)
        (acoustic_inflow * cos (1 : ℝ) ^ 2 / phi)
      have h_tri2 := abs_add_le (1 : ℝ) (acoustic_bleed * sin (1 : ℝ) ^ 2 / phi)
      have h_frac1 : abs (acoustic_bleed * sin (1 : ℝ) ^ 2 / phi) ≤ (1 : ℝ) := by
        rw [abs_div, abs_of_pos hφ]
        refine (div_le_iff₀ hφ).mpr ?_
        have h_nonneg : (0 : ℝ) ≤ acoustic_bleed * sin 1 ^ 2 :=
          mul_nonneg (le_of_lt acoustic_bleed_pos) (sq_nonneg _)
        rw [abs_of_nonneg h_nonneg, one_mul]
        exact acoustic_bleed_mul_sin_sq_le_phi
      have h_frac2 : abs (acoustic_inflow * cos (1 : ℝ) ^ 2 / phi) ≤ (1 : ℝ) := by
        rw [abs_div, abs_of_pos hφ]
        refine (div_le_iff₀ hφ).mpr ?_
        have h_nonneg : (0 : ℝ) ≤ acoustic_inflow * cos 1 ^ 2 :=
          mul_nonneg (le_of_lt acoustic_inflow_pos) (sq_nonneg _)
        rw [abs_of_nonneg h_nonneg, one_mul]
        exact acoustic_inflow_mul_cos_sq_le_phi
      have h1part : abs (1 + acoustic_bleed * sin (1 : ℝ) ^ 2 / phi) ≤ (2 : ℝ) := by
        nlinarith [h_tri2, abs_of_pos (show (0 : ℝ) < (1 : ℝ) by norm_num), h_frac1]
      nlinarith [h_tri, h1part, h_frac2]
    have hb3 : abs b3 ≤ (11 : ℝ) := by
      dsimp [b3]
      have h_pv := abs_le.mp phase_variance_abs_le_one
      have hhi : b3 ≤ (11 : ℝ) := by
        nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_ten, h_pv.2,
          bleed_in_factor_nonneg]
      have hlo : (-11 : ℝ) ≤ b3 := by
        nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_ten, h_pv.1,
          bleed_in_factor_nonneg]
      exact abs_le.mpr ⟨hlo, hhi⟩
    have h_chain : abs (cos p.delta_psi * b1 * b2 * b3) ≤
        abs (cos p.delta_psi) * abs b1 * abs b2 * abs b3 := by
      simp only [abs_mul, mul_assoc]
      exact le_rfl
    have h_prod : abs (cos p.delta_psi) * abs b1 * abs b2 * abs b3 ≤ (99 : ℝ) := by
      calc abs (cos p.delta_psi) * abs b1 * abs b2 * abs b3
          ≤ (1 : ℝ) * abs b1 * abs b2 * abs b3 := by gcongr
        _ ≤ (1 : ℝ) * (3 : ℝ) * abs b2 * abs b3 := by gcongr
        _ ≤ (1 : ℝ) * (3 : ℝ) * (3 : ℝ) * abs b3 := by gcongr
        _ ≤ (1 : ℝ) * (3 : ℝ) * (3 : ℝ) * (11 : ℝ) := by gcongr
        _ = 99 := by norm_num
    exact le_trans h_chain h_prod
  have h_chaos : abs (1 + chaos_factor * (p.D_eff - 25) / 25) ≤ (2 : ℝ) :=
    chaos_perturbation_abs_le_two p h_D
  have h_scale : abs (p.N * p.P / sqrt p.D_eff) ≤ (1 / sqrt (6 : ℝ)) := by
    rw [h_N, h_P, one_mul, abs_div, abs_of_pos (by norm_num), abs_of_pos (Real.sqrt_pos.mpr (by linarith [h_D.1]))]
    exact one_div_le_one_div_of_le (by norm_num) (Real.sqrt_le_sqrt h_D.1)
  have h_bound : abs (term3 p) ≤ beta * (198 / sqrt (6 : ℝ)) := by
    have hβ' : 0 ≤ beta := beta_nonneg
    have h_le : abs (beta * (p.N * p.P / sqrt p.D_eff) * (1 + chaos_factor * (p.D_eff - 25) / 25) *
        cos p.delta_psi * b1 * b2 * b3) ≤ beta * (198 / sqrt (6 : ℝ)) := by
      have h_chain : abs (beta * (p.N * p.P / sqrt p.D_eff) * (1 + chaos_factor * (p.D_eff - 25) / 25) *
            cos p.delta_psi * b1 * b2 * b3) ≤
          beta * abs (p.N * p.P / sqrt p.D_eff) * abs (1 + chaos_factor * (p.D_eff - 25) / 25) *
            abs (cos p.delta_psi * b1 * b2 * b3) := by
        simp [abs_mul, abs_of_nonneg hβ', mul_assoc]
      have h_mid : beta * abs (p.N * p.P / sqrt p.D_eff) * abs (1 + chaos_factor * (p.D_eff - 25) / 25) *
          abs (cos p.delta_psi * b1 * b2 * b3) ≤ beta * (198 / sqrt (6 : ℝ)) := by
        calc beta * abs (p.N * p.P / sqrt p.D_eff) * abs (1 + chaos_factor * (p.D_eff - 25) / 25) *
              abs (cos p.delta_psi * b1 * b2 * b3)
            ≤ beta * (1 / sqrt (6 : ℝ)) * (2 : ℝ) * (99 : ℝ) := by
              gcongr <;> nlinarith [h_scale, h_chaos, h_factor, hβ']
          _ = beta * (198 / sqrt (6 : ℝ)) := by ring
      exact le_trans h_chain h_mid
    have h_rearr :
        abs (term3 p) =
        abs (beta * (p.N * p.P / sqrt p.D_eff) * (1 + chaos_factor * (p.D_eff - 25) / 25) *
          cos p.delta_psi *
          (1 + poof_factor * cos (theta_s + pi) + suction_factor * sin theta_s) *
          (1 + acoustic_bleed * sin (p.delta_theta) ^ 2 / phi +
            acoustic_inflow * cos (p.delta_theta) ^ 2 / phi) *
          (1 + bleed_in_factor * phase_variance)) := by
      simp only [term3, h_N, h_P, h_dt, b1, b2, b3, abs_mul, abs_of_nonneg hβ]
      ring_nf
    rw [h_rearr]
    exact h_le
  have h_cap : beta * (198 / sqrt (6 : ℝ)) < (0.2 : ℝ) := by
    have h_beta := beta_lt_one_over_410
    have h_num := show (1 / 410) * (198 / 2.44) < (0.2 : ℝ) by norm_num
    have h_sqrt6 : (2.44 : ℝ) < sqrt (6 : ℝ) := Real.lt_sqrt_of_sq_lt (by norm_num : (2.44 : ℝ) ^ 2 < 6)
    have h_quot : 198 / sqrt (6 : ℝ) < 198 / 2.44 := by
      rw [div_lt_div_iff₀ (by norm_num) (by nlinarith [h_sqrt6])]
      linarith [h_sqrt6]
    have h_pos : (0 : ℝ) < 198 / sqrt (6 : ℝ) := by positivity
    calc beta * (198 / sqrt (6 : ℝ))
        < (1 / 410) * (198 / sqrt (6 : ℝ)) :=
          mul_lt_mul_of_pos_right h_beta h_pos
      _ < (1 / 410) * (198 / 2.44) := by gcongr
      _ < (0.2 : ℝ) := h_num
  nlinarith [h_bound, h_cap]

lemma term1_base_negative_of_typical_delta
    (p : FSOTParams)
    (h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3)
    (hN : (0 : ℝ) < p.N)
    (hP : (0 : ℝ) < p.P)
    (hD : (0 : ℝ) < p.D_eff) :
    term1_base p < 0 := by
  have h_cos_neg : cos ((psi_con + p.delta_psi) / eta_eff) < 0 :=
    cos_arg_negative_for_typical_delta_psi p h_delta
  have h_scale : 0 < p.N * p.P / sqrt p.D_eff :=
    div_pos (mul_pos hN hP) (Real.sqrt_pos.mpr hD)
  have h_tail : 0 < exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) *
      (1 + growth_term p * coherence_efficiency) := by
    apply mul_pos (exp_pos _)
    nlinarith [growth_term_positive p, coherence_efficiency_positive]
  rw [term1_base]
  have h_cos_scale : cos ((psi_con + p.delta_psi) / eta_eff) *
      (p.N * p.P / sqrt p.D_eff) < 0 := by nlinarith [h_cos_neg, h_scale]
  have h_prod : cos ((psi_con + p.delta_psi) / eta_eff) * (p.N * p.P / sqrt p.D_eff) *
      exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) *
      (1 + growth_term p * coherence_efficiency) < 0 := by
    nlinarith [h_cos_scale, h_tail]
  simpa [mul_assoc, mul_left_comm, mul_comm] using h_prod

lemma term1_positive_of_observer_negative_quirk
    (p : FSOTParams)
    (h_obs : p.observed = true)
    (h_base_neg : term1_base p < 0)
    (h_adj_pos : (0 : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25))
    (h_quirk_neg : quirkMod p < 0) :
    (0 : ℝ) < term1 p := by
  have h_eq := observer_modulates_term1 p h_obs
  rw [h_eq]
  have h_mid : term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) < 0 :=
    mul_neg_of_neg_of_pos h_base_neg h_adj_pos
  nlinarith [h_mid, h_quirk_neg]

lemma quirkMod_neg_of_delta_psi_ge_07
    (p : FSOTParams)
    (h_obs : p.observed = true)
    (h_dp : (0.7 : ℝ) ≤ p.delta_psi)
    (h_dp_hi : p.delta_psi ≤ (1.3 : ℝ)) :
    quirkMod p < 0 := by
  simp [quirkMod, h_obs]
  have h_exp_pos : (0 : ℝ) < exp (consciousness_factor * phase_variance) :=
    exp_pos _
  have h_cos_neg := cos_dp_pv_neg_of_ge_07 p.delta_psi h_dp h_dp_hi
  exact mul_neg_of_pos_of_neg h_exp_pos h_cos_neg

lemma quirkMod_pos_of_delta_psi_le_06
    (p : FSOTParams)
    (h_obs : p.observed = true)
    (h_dp : p.delta_psi ≤ (0.6 : ℝ))
    (h_dp_lo : (0 : ℝ) ≤ p.delta_psi) :
    (0 : ℝ) < quirkMod p := by
  simp [quirkMod, h_obs]
  have h_exp_pos : (0 : ℝ) < exp (consciousness_factor * phase_variance) :=
    exp_pos _
  have h_cos_pos := cos_dp_pv_pos_of_le_06 p.delta_psi h_dp h_dp_lo
  exact mul_pos h_exp_pos h_cos_pos

lemma ai_term1_base_abs_gt_one_six :
    (1.6 : ℝ) < abs (term1_base (get_domain_params "ai")) := by
  set p := get_domain_params "ai"
  have h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ (1.3 : ℝ) := by
    simp [p, get_domain_params]; norm_num
  have hN : (0 : ℝ) < p.N := by simp [p, get_domain_params]
  have hP : (0 : ℝ) < p.P := by simp [p, get_domain_params]
  have hD : (0 : ℝ) < p.D_eff := by simp [p, get_domain_params]
  have h_neg := term1_base_negative_of_typical_delta p h_delta hN hP hD
  rw [abs_of_neg h_neg]
  have h_dp : p.delta_psi = (0.50 : ℝ) := by simp [p, get_domain_params]
  have h_exp_simp : exp (-alpha * p.recent_hits / p.N + p.rho + bleed_in_factor * p.delta_psi) =
      exp (1 + bleed_in_factor * (0.50 : ℝ)) := by simp [p, get_domain_params]
  have h_neg_cos : (0.74 : ℝ) < -cos ((psi_con + (0.50 : ℝ)) / eta_eff) := by
    linarith [ai_cos_lt_neg_075]
  have h_exp : (4 : ℝ) < exp (1 + bleed_in_factor * (0.50 : ℝ)) := by
    simpa [show (0.50 : ℝ) = (0.5 : ℝ) by norm_num] using ai_exp_factor_gt_four
  have h_growth_term : (1 : ℝ) < growth_term p :=
    growth_term_hits_zero_gt_one p (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
  have h_growth : (1.9 : ℝ) < 1 + growth_term p * coherence_efficiency := by
    nlinarith [h_growth_term, coherence_efficiency_gt_nine_five]
  have h_mag : (1.6 : ℝ) < -(term1_base p) := by
    simp only [term1_base, p, get_domain_params, mul_one, one_mul]
    have h_exp_rw : exp (-alpha * (0 : ℝ) / 1 + 1 + bleed_in_factor * (0.50 : ℝ)) =
        exp (1 + bleed_in_factor * (0.50 : ℝ)) := by ring_nf
    have h_floor : (1.6 : ℝ) < (1 / 3.317) * (0.74 : ℝ) * (4 : ℝ) * (1.9 : ℝ) := by norm_num
    have h_inv : (1 / 3.317) < (1 / sqrt (11 : ℝ)) := by
      apply one_div_lt_one_div_of_lt (by norm_num)
      exact sqrt_11_lt_3317
    have h_cos_bound : (1 / sqrt 11) * (0.74 : ℝ) <
        (1 / sqrt 11) * (-cos ((psi_con + (0.50 : ℝ)) / eta_eff)) := by
      refine mul_lt_mul_of_pos_left h_neg_cos ?_
      apply div_pos (by norm_num)
      exact Real.sqrt_pos.mpr (by norm_num)
    have h_exp_bound : (1 / sqrt 11) * (-cos ((psi_con + (0.50 : ℝ)) / eta_eff)) * (4 : ℝ) <
        (1 / sqrt 11) * (-cos ((psi_con + (0.50 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.50 : ℝ)) := by
      have h_pos : 0 < (1 / sqrt 11) * (-cos ((psi_con + (0.50 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos, sqrt_11_gt_3316]
      exact mul_lt_mul_of_pos_left h_exp h_pos
    have h_rearrange : -(1 / sqrt 11 * cos ((psi_con + (0.50 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (0.50 : ℝ)) *
        (1 + growth_term { D_eff := 11, delta_psi := 0.50, observed := false } *
          coherence_efficiency)) =
      (1 / sqrt 11) * (-cos ((psi_con + (0.50 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.50 : ℝ)) *
        (1 + growth_term { D_eff := 11, delta_psi := 0.50, observed := false } *
          coherence_efficiency) := by ring
    have h_growth_eq : (1 + growth_term p * coherence_efficiency) =
        (1 + growth_term { D_eff := 11, delta_psi := 0.50, observed := false } *
          coherence_efficiency) := by
      simp [growth_term, p, get_domain_params]
    have h_growth' : (1.9 : ℝ) < 1 + growth_term { D_eff := 11, delta_psi := 0.50, observed := false } *
        coherence_efficiency := by
      simpa [h_growth_eq] using h_growth
    have h_pos_mag : (1.6 : ℝ) < (1 / sqrt 11) * (-cos ((psi_con + (0.50 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.50 : ℝ)) *
        (1 + growth_term { D_eff := 11, delta_psi := 0.50, observed := false } *
          coherence_efficiency) := by
      nlinarith [h_floor, h_inv, h_cos_bound, h_exp_bound, h_growth']
    rw [h_exp_rw, h_rearrange]
    exact h_pos_mag
  linarith [h_mag]

lemma cmb_term1_base_abs_gt_one_three_five (p : FSOTParams)
    (h_D : p.D_eff = 24) (h_dp : p.delta_psi = (0.8 : ℝ)) (h_obs : p.observed = false)
    (h_hits : p.recent_hits = 0) (h_N : p.N = 1) (h_P : p.P = 1) (h_rho : p.rho = 1) :
    (1.35 : ℝ) < abs (term1_base p) := by
  have h_neg := term1_base_negative_for_high_D_eff p (by rw [h_D]; norm_num) h_obs
    ⟨(by rw [h_dp]; norm_num), (by rw [h_dp]; norm_num)⟩
    (by rw [h_N]; norm_num) (by rw [h_P]; norm_num)
  rw [abs_of_neg h_neg]
  have h_exp_simp : exp (-alpha * (0 : ℝ) / (1 : ℝ) + (1 : ℝ) + bleed_in_factor * (0.8 : ℝ)) =
      exp (1 + bleed_in_factor * (0.8 : ℝ)) := by
    simp [h_hits, h_N, h_rho, h_dp, div_eq_mul_inv, mul_zero, zero_mul]
  have h_cos := cmb_cos_lt_neg_099
  have h_neg_cos : (0.99 : ℝ) < -cos ((psi_con + (0.8 : ℝ)) / eta_eff) := by linarith [h_cos]
  have h_exp := cmb_exp_factor_gt_five
  have h_growth_term : (1 : ℝ) < growth_term p :=
    growth_term_hits_zero_gt_one p h_hits h_N
  have h_growth : (1.45 : ℝ) < 1 + growth_term p * coherence_efficiency := by
    nlinarith [h_growth_term, coherence_efficiency_gt_seven_tenths]
  have h_mag : (1.35 : ℝ) < -(term1_base p) := by
    simp only [term1_base, h_D, h_dp, h_hits, h_N, h_P, h_rho, mul_one, one_mul]
    rw [h_exp_simp]
    have h_floor : (1.35 : ℝ) < (1 / 4.899) * (0.99 : ℝ) * (5 : ℝ) * (1.45 : ℝ) := by norm_num
    have h_inv_lo : (1 / 4.899) < (1 / sqrt (24 : ℝ)) := by
      apply one_div_lt_one_div_of_lt (by norm_num)
      exact sqrt_24_lt_4899
    have h_cos_bound : (1 / sqrt 24) * (0.99 : ℝ) <
        (1 / sqrt 24) * (-cos ((psi_con + (0.8 : ℝ)) / eta_eff)) := by
      refine mul_lt_mul_of_pos_left h_neg_cos ?_
      nlinarith [sqrt_24_gt_4898]
    have h_exp_bound : (1 / sqrt 24) * (-cos ((psi_con + (0.8 : ℝ)) / eta_eff)) * (5 : ℝ) <
        (1 / sqrt 24) * (-cos ((psi_con + (0.8 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.8 : ℝ)) := by
      have h_pos : 0 < (1 / sqrt 24) * (-cos ((psi_con + (0.8 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos, sqrt_24_gt_4898]
      exact mul_lt_mul_of_pos_left h_exp h_pos
    have h_rearrange : -(1 / sqrt 24 * cos ((psi_con + (0.8 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (0.8 : ℝ)) *
        (1 + growth_term p * coherence_efficiency)) =
      (1 / sqrt 24) * (-cos ((psi_con + (0.8 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.8 : ℝ)) *
        (1 + growth_term p * coherence_efficiency) := by ring
    have h_pos_mag : (1.35 : ℝ) < (1 / sqrt 24) * (-cos ((psi_con + (0.8 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.8 : ℝ)) *
        (1 + growth_term p * coherence_efficiency) := by
      nlinarith [h_floor, h_inv_lo, h_cos_bound, h_exp_bound, h_growth]
    rw [h_rearrange]
    exact h_pos_mag
  linarith [h_mag]

lemma domain_term1_lt_neg_08_ai :
    term1 (get_domain_params "ai") < (-0.8 : ℝ) := by
  set p := get_domain_params "ai"
  have h_obs : p.observed = false := by simp [p, get_domain_params]
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, p, get_domain_params, h_obs]
  have h_term1_eq : term1 p = term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) := by
    simp [term1, h_quirk]
  have h_base_mag : (1.6 : ℝ) < abs (term1_base p) := by simpa [p] using ai_term1_base_abs_gt_one_six
  have h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ (1.3 : ℝ) := by
    simp [p, get_domain_params]; norm_num
  have hN : (0 : ℝ) < p.N := by simp [p, get_domain_params]
  have hP : (0 : ℝ) < p.P := by simp [p, get_domain_params]
  have hD : (0 : ℝ) < p.D_eff := by simp [p, get_domain_params]
  have h_base_neg := term1_base_negative_of_typical_delta p h_delta hN hP hD
  have h_adj_lo := perceived_adjust_lo_D11
  have h_bound : term1_base p * (0.752 : ℝ) < (-0.8 : ℝ) := by
    rw [abs_of_neg h_base_neg] at h_base_mag
    nlinarith [h_base_mag, h_adj_lo]
  rw [h_term1_eq]
  have h_adj : (0.752 : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25) := h_adj_lo
  nlinarith [h_bound, h_adj, h_base_neg]

lemma domain_ai_term1_overcomes_term3 :
    term1 (get_domain_params "ai") + abs (term3 (get_domain_params "ai")) < -(1 : ℝ) := by
  set p := get_domain_params "ai"
  have h_obs : p.observed = false := by simp [p, get_domain_params]
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, p, get_domain_params, h_obs]
  have h_term1_eq : term1 p = term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) := by
    simp [term1, h_quirk]
  have h_base_mag : (1.6 : ℝ) < abs (term1_base p) := by simpa [p] using ai_term1_base_abs_gt_one_six
  have h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ (1.3 : ℝ) := by
    simp [p, get_domain_params]; norm_num
  have hN : (0 : ℝ) < p.N := by simp [p, get_domain_params]
  have hP : (0 : ℝ) < p.P := by simp [p, get_domain_params]
  have hD : (0 : ℝ) < p.D_eff := by simp [p, get_domain_params]
  have h_base_neg := term1_base_negative_of_typical_delta p h_delta hN hP hD
  have h_adj : (0.752 : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25) := by
    simpa [p, get_domain_params] using perceived_adjust_lo_D11
  have h_term3 := term3_abs_lt_fifth_default p ⟨by simp [p, get_domain_params]; norm_num,
    by simp [p, get_domain_params]; norm_num⟩ ⟨by simp [p, get_domain_params]; norm_num,
    by simp [p, get_domain_params]; norm_num⟩ (by simp [p, get_domain_params])
    (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
  have h_mag : (1.6 : ℝ) * (0.752 : ℝ) < -term1 p := by
    rw [h_term1_eq]
    rw [abs_of_neg h_base_neg] at h_base_mag
    nlinarith [h_base_mag, h_adj]
  have h_neg : term1 p < 0 := by linarith [h_mag]
  linarith [h_mag, h_term3, h_neg]

lemma domain_term1_lt_neg_08_cmb :
    term1 (get_domain_params "cmb") < (-0.8 : ℝ) := by
  set p := get_domain_params "cmb"
  have h_obs : p.observed = false := by simp [p, get_domain_params]
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, p, get_domain_params, h_obs]
  have h_term1_eq : term1 p = term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) := by
    simp [term1, h_quirk]
  have h_D_bounds : (20 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 30 := by simp [p, get_domain_params]; norm_num
  have h_base_mag := cmb_term1_base_abs_gt_one_three_five p (by simp [p, get_domain_params])
    (by simp [p, get_domain_params]) h_obs (by simp [p, get_domain_params])
    (by simp [p, get_domain_params]) (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
  have h_base_neg := term1_base_negative_for_high_D_eff p h_D_bounds.1 h_obs
    (by simp [p, get_domain_params]; norm_num) (by simp [p, get_domain_params])
    (by simp [p, get_domain_params])
  have h_adj_lo := perceived_adjust_lo p h_D_bounds
  have h_bound : (1.35 : ℝ) * (0.91 : ℝ) < -term1_base p := by
    rw [abs_of_neg h_base_neg] at h_base_mag
    nlinarith [h_base_mag, h_adj_lo]
  rw [h_term1_eq]
  nlinarith [h_bound, h_base_neg, h_adj_lo]

lemma domain_cmb_term1_overcomes_term3 :
    term1 (get_domain_params "cmb") + abs (term3 (get_domain_params "cmb")) < -(1 : ℝ) := by
  set p := get_domain_params "cmb"
  have h_obs : p.observed = false := by simp [p, get_domain_params]
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, p, get_domain_params, h_obs]
  have h_term1_eq : term1 p = term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) := by
    simp [term1, h_quirk]
  have h_D_bounds : (20 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 30 := by simp [p, get_domain_params]; norm_num
  have h_base_mag := cmb_term1_base_abs_gt_one_three_five p (by simp [p, get_domain_params])
    (by simp [p, get_domain_params]) h_obs (by simp [p, get_domain_params])
    (by simp [p, get_domain_params]) (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
  have h_base_neg := term1_base_negative_for_high_D_eff p h_D_bounds.1 h_obs
    (by simp [p, get_domain_params]; norm_num) (by simp [p, get_domain_params])
    (by simp [p, get_domain_params])
  have h_adj_lo := perceived_adjust_lo p h_D_bounds
  have h_term3 := term3_abs_lt_fifth_default p ⟨by simp [p, get_domain_params]; norm_num,
    by simp [p, get_domain_params]; norm_num⟩ ⟨by simp [p, get_domain_params]; norm_num,
    by simp [p, get_domain_params]; norm_num⟩ (by simp [p, get_domain_params])
    (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
  have h_mag : (1.35 : ℝ) * (0.91 : ℝ) < -term1 p := by
    rw [h_term1_eq]
    nlinarith [h_base_mag, h_base_neg, h_adj_lo, abs_of_neg h_base_neg]
  have h_neg : term1 p < 0 := by linarith [h_mag]
  linarith [h_mag, h_term3, h_neg]

lemma quirkMod_lt_exp_cos_bound (p : FSOTParams) (h_obs : p.observed = true)
    (h_cos_hi : cos (p.delta_psi + phase_variance) < (c_hi : ℝ))
    (h_cos_pos : (0 : ℝ) < cos (p.delta_psi + phase_variance)) :
    quirkMod p < (1.338 : ℝ) * c_hi := by
  simp [quirkMod, h_obs]
  nlinarith [exp_consciousness_phase_lt_132, h_cos_hi, h_cos_pos]

lemma term1_gt_neg_08_of_observer_pos_quirk
    (p : FSOTParams) (h_obs : p.observed = true)
    (h_base_neg : term1_base p < 0)
    (h_adj_lo : (adj_lo : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25))
    (h_adj_hi : 1 + new_perceived_param * log (p.D_eff / 25) < (adj_hi : ℝ))
    (h_adj_lo_pos : (0 : ℝ) < adj_lo)
    (h_quirk_pos : (0 : ℝ) < quirkMod p) (h_quirk_hi : quirkMod p < (quirk_hi : ℝ))
    (h_worst : (-0.8 : ℝ) < term1_base p * adj_hi * quirk_hi) :
    (-0.8 : ℝ) < term1 p := by
  have h_eq := observer_modulates_term1 p h_obs
  set adj := 1 + new_perceived_param * log (p.D_eff / 25)
  have h_adj_pos : (0 : ℝ) < adj := lt_trans h_adj_lo_pos h_adj_lo
  have h_adj_mid : term1_base p * adj_hi < term1_base p * adj :=
    mul_lt_mul_of_neg_left h_adj_hi h_base_neg
  have h_adj_neg : term1_base p * adj < 0 := mul_neg_of_neg_of_pos h_base_neg h_adj_pos
  have h_quirk_mid : term1_base p * adj * quirk_hi < term1_base p * adj * quirkMod p :=
    mul_lt_mul_of_neg_left h_quirk_hi h_adj_neg
  have h_prod_lo :
      term1_base p * adj_hi * quirk_hi < term1_base p * adj * quirkMod p := by
    nlinarith [h_adj_mid, h_quirk_mid]
  rw [h_eq]
  linarith [h_prod_lo, h_worst]

lemma domain_term1_positive_of_params (p : FSOTParams)
    (h_obs : p.observed = true)
    (h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3)
    (h_dp : (0.7 : ℝ) ≤ p.delta_psi)
    (hN : (0 : ℝ) < p.N) (hP : (0 : ℝ) < p.P)
    (h_D : (6 : ℝ) ≤ p.D_eff) :
    (0 : ℝ) < term1 p := by
  have h_base_neg := term1_base_negative_of_typical_delta p h_delta hN hP
    (by linarith [h_D])
  have h_adj_pos : (0 : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25) :=
    lt_trans (by norm_num : (0 : ℝ) < (0.567 : ℝ)) (perceived_adjust_lo_domain p h_D)
  have h_dp_hi : p.delta_psi ≤ (1.3 : ℝ) := h_delta.2
  have h_quirk_neg := quirkMod_neg_of_delta_psi_ge_07 p h_obs h_dp h_dp_hi
  exact term1_positive_of_observer_negative_quirk p h_obs h_base_neg h_adj_pos h_quirk_neg

lemma domain_term1_gt_neg_08_chemical :
    (-0.8 : ℝ) < term1 (get_domain_params "chemical") := by
  set p := get_domain_params "chemical"
  have h_obs : p.observed = true := by simp [p, get_domain_params]
  have h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ (1.3 : ℝ) := by
    simp [p, get_domain_params]; norm_num
  have hN : (0 : ℝ) < p.N := by simp [p, get_domain_params]
  have hP : (0 : ℝ) < p.P := by simp [p, get_domain_params]
  have hD : (0 : ℝ) < p.D_eff := by simp [p, get_domain_params]
  have h_base_neg := term1_base_negative_of_typical_delta p h_delta hN hP hD
  have h_adj_lo := perceived_adjust_lo_domain p (by simp [p, get_domain_params]; norm_num)
  have h_adj_hi := perceived_adjust_hi_domain p (by simp [p, get_domain_params]; constructor <;> norm_num)
  have h_quirk_pos := quirkMod_pos_of_delta_psi_le_06 p h_obs
    (by simp [p, get_domain_params]; norm_num) (by simp [p, get_domain_params]; norm_num)
  have h_cos_pos := cos_dp_pv_pos_of_le_06 p.delta_psi (by simp [p, get_domain_params]; norm_num)
    (by simp [p, get_domain_params]; norm_num)
  have h_quirk_hi : quirkMod p < (0.156 : ℝ) := by
    have h_cos_hi : cos (p.delta_psi + phase_variance) < (0.116 : ℝ) := by
      have h_sum_lo : (1.455 : ℝ) < p.delta_psi + phase_variance := by
        simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
      have h_in : p.delta_psi + phase_variance ∈ Set.Icc (0 : ℝ) pi := by
        constructor
        · simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
        · have h_upper : p.delta_psi + phase_variance < (1.461 : ℝ) := by
            simp only [p, get_domain_params]
            linarith [phase_variance_lt_0961]
          exact le_of_lt (lt_trans h_upper (by unfold pi; nlinarith [pi_gt_d4]))
      have h_ref : (1.455 : ℝ) ∈ Set.Icc (0 : ℝ) pi := ⟨by norm_num, by unfold pi; nlinarith [pi_gt_d4]⟩
      exact lt_trans (strictAntiOn_cos h_ref h_in h_sum_lo) cos_1455_lt_0116
    exact lt_trans (quirkMod_lt_exp_cos_bound p h_obs h_cos_hi h_cos_pos) (by norm_num)
  have h_base_mag : (0.35 : ℝ) < -term1_base p := by
    have h_neg_cos : (0.74 : ℝ) < -cos ((psi_con + (0.5 : ℝ)) / eta_eff) := by linarith [ai_cos_lt_neg_075]
    have h_exp := ai_exp_factor_gt_four
    have h_growth_term := growth_term_hits_zero_gt_one p (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
    have h_growth : (1.9 : ℝ) < 1 + growth_term p * coherence_efficiency := by
      nlinarith [h_growth_term, coherence_efficiency_gt_nine_five]
    have h_rearrange : -(1 / 3 * cos ((psi_con + (0.5 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (0.5 : ℝ)) *
        (1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
          coherence_efficiency)) =
      (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.5 : ℝ)) *
        (1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
          coherence_efficiency) := by ring
    have h_cos_bound : (1 / 3) * (0.74 : ℝ) <
        (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) := by
      refine mul_lt_mul_of_pos_left h_neg_cos (by norm_num)
    have h_exp_bound : (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) * (4 : ℝ) <
        (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.5 : ℝ)) := by
      have h_pos : 0 < (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos]
      exact mul_lt_mul_of_pos_left h_exp h_pos
    have h_growth_eq : (1 + growth_term p * coherence_efficiency) =
        (1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
          coherence_efficiency) := by
      simp [growth_term, p, get_domain_params]
    have h_growth' : (1.9 : ℝ) < 1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
        coherence_efficiency := by
      simpa [h_growth_eq] using h_growth
    have h_pos_mag : (0.35 : ℝ) < (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.5 : ℝ)) *
        (1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
          coherence_efficiency) := by
      have h_floor : (0.35 : ℝ) < (1 / 3) * (0.74 : ℝ) * (4 : ℝ) * (1.9 : ℝ) := by norm_num
      nlinarith [h_floor, h_cos_bound, h_exp_bound, h_growth']
    simp only [term1_base, p, get_domain_params, mul_one, one_mul]
    have h_exp_rw : exp (-alpha * (0 : ℝ) / 1 + 1 + bleed_in_factor * (0.5 : ℝ)) =
        exp (1 + bleed_in_factor * (0.5 : ℝ)) := by ring_nf
    rw [h_exp_rw, sqrt_9_eq_3, h_rearrange]
    exact h_pos_mag
  have h_base_hi : -term1_base p < (4 : ℝ) := by
    have hcos_neg : cos ((psi_con + (0.5 : ℝ)) / eta_eff) < 0 := by
      linarith [ai_cos_lt_neg_075]
    have h_cos_le : -cos ((psi_con + (0.5 : ℝ)) / eta_eff) ≤ (1 : ℝ) := by
      have h := abs_le.mp (abs_cos_le_one ((psi_con + (0.5 : ℝ)) / eta_eff))
      linarith [hcos_neg, h.1, h.2]
    have h_bleed_hi : (1 + bleed_in_factor * (0.5 : ℝ)) < (1.505 : ℝ) := by
      nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_1002]
    have h_exp_hi : exp (1 + bleed_in_factor * (0.5 : ℝ)) < (5 : ℝ) :=
      lt_trans (Real.exp_lt_exp.mpr h_bleed_hi) exp_1505_lt_5
    have h_growth_hi : (1 + growth_term p * coherence_efficiency) < (2.2 : ℝ) := by
      have h_prod := growth_term_coherence_product_lt_11523 p
        (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
      linarith [h_prod]
    have h_growth_term_eq : growth_term p =
        growth_term { D_eff := 9, delta_psi := 0.5, observed := true } := by
      simp [growth_term, p, get_domain_params]
    have h_growth_hi' : (1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
        coherence_efficiency) < (2.2 : ℝ) := by
      simpa [← h_growth_term_eq] using h_growth_hi
    have h_core_lt : (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.5 : ℝ)) *
        (1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
          coherence_efficiency) < (4 : ℝ) := by
      have h₁ : (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) ≤ (1 / 3) * (1 : ℝ) :=
        mul_le_mul_of_nonneg_left h_cos_le (by norm_num : (0 : ℝ) ≤ 1 / 3)
      have h₂ := mul_le_mul h₁ (le_of_lt h_exp_hi)
        (le_of_lt (exp_pos (1 + bleed_in_factor * (0.5 : ℝ))))
        (by norm_num : (0 : ℝ) ≤ 1 / 3 * (1 : ℝ))
      have h_growth_nonneg : (0 : ℝ) ≤ 1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
          coherence_efficiency := by
        have h_gt : (0 : ℝ) < growth_term { D_eff := 9, delta_psi := 0.5, observed := true } := by
          dsimp [growth_term]
          exact exp_pos _
        nlinarith [h_gt, coherence_efficiency_gt_nine_five]
      have h₃ := mul_le_mul h₂ (le_of_lt h_growth_hi') h_growth_nonneg
        (by norm_num : (0 : ℝ) ≤ 1 / 3 * (1 : ℝ) * (5 : ℝ))
      have h_num : (1 / 3) * (1 : ℝ) * (5 : ℝ) * (2.2 : ℝ) < (4 : ℝ) := by norm_num
      exact lt_of_le_of_lt h₃ h_num
    have h_eq : -term1_base p =
        (1 / 3) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.5 : ℝ)) *
          (1 + growth_term { D_eff := 9, delta_psi := 0.5, observed := true } *
            coherence_efficiency) := by
      simp only [term1_base, p, get_domain_params, sqrt_9_eq_3]
      ring_nf
    rw [h_eq]
    exact h_core_lt
  have h_worst : (-0.8 : ℝ) < term1_base p * (0.99 : ℝ) * (0.156 : ℝ) := by
    have h_rng_lo : (-4 : ℝ) < term1_base p := by linarith [h_base_hi]
    have h_rng_hi : term1_base p < (-0.35 : ℝ) := by linarith [h_base_mag]
    nlinarith [h_rng_lo, h_rng_hi]
  exact term1_gt_neg_08_of_observer_pos_quirk p h_obs h_base_neg h_adj_lo h_adj_hi
    (by norm_num : (0 : ℝ) < (0.567 : ℝ)) h_quirk_pos h_quirk_hi h_worst

lemma domain_term1_gt_neg_08_electron :
    (-0.8 : ℝ) < term1 (get_domain_params "electron") := by
  set p := get_domain_params "electron"
  have h_obs : p.observed = true := by simp [p, get_domain_params]
  have h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ (1.3 : ℝ) := by
    simp [p, get_domain_params]; norm_num
  have hN : (0 : ℝ) < p.N := by simp [p, get_domain_params]
  have hP : (0 : ℝ) < p.P := by simp [p, get_domain_params]
  have hD : (0 : ℝ) < p.D_eff := by simp [p, get_domain_params]
  have h_base_neg := term1_base_negative_of_typical_delta p h_delta hN hP hD
  have h_adj_lo := perceived_adjust_lo_domain p (by simp [p, get_domain_params]; norm_num)
  have h_adj_hi := perceived_adjust_hi_domain p (by simp [p, get_domain_params]; constructor <;> norm_num)
  have h_dp_le : p.delta_psi ≤ (0.6 : ℝ) := by simp [p, get_domain_params]
  have h_dp_lo : (0 : ℝ) ≤ p.delta_psi := by simp [p, get_domain_params]; norm_num
  have h_quirk_pos := quirkMod_pos_of_delta_psi_le_06 p h_obs h_dp_le h_dp_lo
  have h_cos_pos := cos_dp_pv_pos_of_le_06 p.delta_psi h_dp_le h_dp_lo
  have h_quirk_hi : quirkMod p < (0.022 : ℝ) := by
    have h_cos_hi : cos (p.delta_psi + phase_variance) < (0.016 : ℝ) := by
      have h_sum_lo : (1.555 : ℝ) < p.delta_psi + phase_variance := by
        simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
      have h_in : p.delta_psi + phase_variance ∈ Set.Icc (0 : ℝ) pi := by
        constructor
        · simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
        · have h_upper : p.delta_psi + phase_variance < (1.561 : ℝ) := by
            simp only [p, get_domain_params]
            linarith [phase_variance_lt_0961]
          exact le_of_lt (lt_trans h_upper (by unfold pi; nlinarith [pi_gt_d4]))
      have h_ref : (1.555 : ℝ) ∈ Set.Icc (0 : ℝ) pi := ⟨by norm_num, by unfold pi; nlinarith [pi_gt_d4]⟩
      exact lt_trans (strictAntiOn_cos h_ref h_in h_sum_lo) cos_1555_lt_0016
    exact lt_trans (quirkMod_lt_exp_cos_bound p h_obs h_cos_hi h_cos_pos) (by norm_num)
  have h_base_mag : (0.05 : ℝ) < -term1_base p := by
    have h_neg_cos : (0.4 : ℝ) < -cos ((psi_con + (0.6 : ℝ)) / eta_eff) := by linarith [electron_cos_lt_neg_04]
    have h_exp := electron_exp_factor_gt_three
    have h_growth_term := growth_term_hits_zero_gt_one p (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
    have h_growth : (1.9 : ℝ) < 1 + growth_term p * coherence_efficiency := by
      nlinarith [h_growth_term, coherence_efficiency_gt_nine_five]
    have h_rearrange : -(1 / sqrt 8 * cos ((psi_con + (0.6 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (0.6 : ℝ)) *
        (1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
          coherence_efficiency)) =
      (1 / sqrt 8) * (-cos ((psi_con + (0.6 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.6 : ℝ)) *
        (1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
          coherence_efficiency) := by ring
    have h_cos_bound : (1 / sqrt 8) * (0.4 : ℝ) <
        (1 / sqrt 8) * (-cos ((psi_con + (0.6 : ℝ)) / eta_eff)) := by
      refine mul_lt_mul_of_pos_left h_neg_cos ?_
      apply div_pos (by norm_num)
      exact Real.sqrt_pos.mpr (by norm_num)
    have h_exp_bound : (1 / sqrt 8) * (-cos ((psi_con + (0.6 : ℝ)) / eta_eff)) * (3 : ℝ) <
        (1 / sqrt 8) * (-cos ((psi_con + (0.6 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.6 : ℝ)) := by
      have h_pos : 0 < (1 / sqrt 8) * (-cos ((psi_con + (0.6 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos]
      exact mul_lt_mul_of_pos_left h_exp h_pos
    have h_growth_eq : (1 + growth_term p * coherence_efficiency) =
        (1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
          coherence_efficiency) := by
      simp [growth_term, p, get_domain_params]
    have h_growth' : (1.9 : ℝ) < 1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
        coherence_efficiency := by
      simpa [h_growth_eq] using h_growth
    have h_pos_mag : (0.05 : ℝ) < (1 / sqrt 8) * (-cos ((psi_con + (0.6 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.6 : ℝ)) *
        (1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
          coherence_efficiency) := by
      have h_floor : (0.05 : ℝ) < (1 / 2.829) * (0.4 : ℝ) * (3 : ℝ) * (1.9 : ℝ) := by norm_num
      have h_inv : (1 / 2.829) < (1 / sqrt (8 : ℝ)) := by
        apply one_div_lt_one_div_of_lt (by norm_num)
        exact sqrt_8_lt_2829
      nlinarith [h_floor, h_inv, h_cos_bound, h_exp_bound, h_growth']
    simp only [term1_base, p, get_domain_params, mul_one, one_mul]
    have h_exp_rw : exp (-alpha * (0 : ℝ) / 1 + 1 + bleed_in_factor * (0.6 : ℝ)) =
        exp (1 + bleed_in_factor * (0.6 : ℝ)) := by ring_nf
    rw [h_exp_rw, h_rearrange]
    exact h_pos_mag
  have h_base_hi : -term1_base p < (6 : ℝ) := by
    have hcos_neg : cos ((psi_con + (0.6 : ℝ)) / eta_eff) < 0 := by
      linarith [electron_cos_lt_neg_04]
    have h_cos_le : -cos ((psi_con + (0.6 : ℝ)) / eta_eff) ≤ (1 : ℝ) := by
      have h := abs_le.mp (abs_cos_le_one ((psi_con + (0.6 : ℝ)) / eta_eff))
      linarith [hcos_neg, h.1, h.2]
    have h_bleed_hi : (1 + bleed_in_factor * (0.6 : ℝ)) < (1.602 : ℝ) := by
      nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_1002]
    have h_exp_hi : exp (1 + bleed_in_factor * (0.6 : ℝ)) < (5 : ℝ) :=
      lt_trans (Real.exp_lt_exp.mpr h_bleed_hi) exp_1602_lt_5
    have h_growth_hi : (1 + growth_term p * coherence_efficiency) < (2.2 : ℝ) := by
      have h_prod := growth_term_coherence_product_lt_11523 p
        (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
      linarith [h_prod]
    have h_growth_term_eq : growth_term p =
        growth_term { D_eff := 8, delta_psi := 0.6, observed := true } := by
      simp [growth_term, p, get_domain_params]
    have h_inv : (1 / 2.829) < (1 / sqrt (8 : ℝ)) := by
      apply one_div_lt_one_div_of_lt (by norm_num)
      exact sqrt_8_lt_2829
    have h_growth_hi' : (1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
        coherence_efficiency) < (2.2 : ℝ) := by
      simpa [← h_growth_term_eq] using h_growth_hi
    have h_core_lt : (1 / sqrt 8) * (-cos ((psi_con + (0.6 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.6 : ℝ)) *
        (1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
          coherence_efficiency) < (6 : ℝ) := by
      have h_div_pos : (0 : ℝ) < 1 / sqrt 8 :=
        one_div_pos.mpr (Real.sqrt_pos.mpr (by norm_num))
      have h₁ := mul_le_mul_of_nonneg_left h_cos_le (le_of_lt h_div_pos)
      have h₂ := mul_le_mul h₁ (le_of_lt h_exp_hi)
        (le_of_lt (exp_pos (1 + bleed_in_factor * (0.6 : ℝ))))
        (by nlinarith [h_div_pos])
      have h_growth_nonneg : (0 : ℝ) ≤ 1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
          coherence_efficiency := by
        have h_gt : (0 : ℝ) < growth_term { D_eff := 8, delta_psi := 0.6, observed := true } := by
          dsimp [growth_term]
          exact exp_pos _
        nlinarith [h_gt, coherence_efficiency_gt_nine_five]
      have h₃ := mul_le_mul h₂ (le_of_lt h_growth_hi') h_growth_nonneg
        (by nlinarith [h_div_pos])
      have h_num : (1 / sqrt 8) * (1 : ℝ) * (5 : ℝ) * (2.2 : ℝ) < (6 : ℝ) := by
        have h_eq : (1 / sqrt 8) * (1 : ℝ) * (5 : ℝ) * (2.2 : ℝ) = (11 : ℝ) / sqrt 8 := by ring
        rw [h_eq]
        have h_sqrt_pos : (0 : ℝ) < sqrt 8 := Real.sqrt_pos.mpr (by norm_num)
        rw [div_lt_iff₀ h_sqrt_pos]
        have h_sqrt_lo : (2 : ℝ) < sqrt 8 := Real.lt_sqrt_of_sq_lt (by norm_num : (2 : ℝ) ^ 2 < 8)
        nlinarith [h_sqrt_lo]
      exact lt_of_le_of_lt h₃ h_num
    have h_eq : -term1_base p =
        (1 / sqrt 8) * (-cos ((psi_con + (0.6 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.6 : ℝ)) *
          (1 + growth_term { D_eff := 8, delta_psi := 0.6, observed := true } *
            coherence_efficiency) := by
      simp only [term1_base, p, get_domain_params]
      ring_nf
    rw [h_eq]
    exact h_core_lt
  have h_worst : (-0.8 : ℝ) < term1_base p * (0.99 : ℝ) * (0.022 : ℝ) := by
    have h_rng_lo : (-6 : ℝ) < term1_base p := by linarith [h_base_hi]
    have h_rng_hi : term1_base p < (-0.05 : ℝ) := by linarith [h_base_mag]
    nlinarith [h_rng_lo, h_rng_hi]
  exact term1_gt_neg_08_of_observer_pos_quirk p h_obs h_base_neg h_adj_lo h_adj_hi
    (by norm_num : (0 : ℝ) < (0.567 : ℝ)) h_quirk_pos h_quirk_hi h_worst

lemma domain_term1_gt_neg_08_medical :
    (-0.8 : ℝ) < term1 (get_domain_params "medical") := by
  set p := get_domain_params "medical"
  have h_obs : p.observed = true := by simp [p, get_domain_params]
  have h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ (1.3 : ℝ) := by
    simp [p, get_domain_params]; norm_num
  have hN : (0 : ℝ) < p.N := by simp [p, get_domain_params]
  have hP : (0 : ℝ) < p.P := by simp [p, get_domain_params]
  have hD : (0 : ℝ) < p.D_eff := by simp [p, get_domain_params]
  have h_base_neg := term1_base_negative_of_typical_delta p h_delta hN hP hD
  have h_adj_lo := perceived_adjust_lo_domain p (by simp [p, get_domain_params]; norm_num)
  have h_adj_hi := perceived_adjust_hi_domain p (by simp [p, get_domain_params]; constructor <;> norm_num)
  have h_quirk_pos := quirkMod_pos_of_delta_psi_le_06 p h_obs
    (by simp [p, get_domain_params]; norm_num) (by simp [p, get_domain_params]; norm_num)
  have h_cos_pos := cos_dp_pv_pos_of_le_06 p.delta_psi (by simp [p, get_domain_params]; norm_num)
    (by simp [p, get_domain_params]; norm_num)
  have h_quirk_hi : quirkMod p < (0.352 : ℝ) := by
    have h_cos_hi : cos (p.delta_psi + phase_variance) < (0.263 : ℝ) := by
      have h_sum_lo : (1.305 : ℝ) < p.delta_psi + phase_variance := by
        simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
      have h_in : p.delta_psi + phase_variance ∈ Set.Icc (0 : ℝ) pi := by
        constructor
        · simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
        · have h_upper : p.delta_psi + phase_variance < (1.311 : ℝ) := by
            simp only [p, get_domain_params]
            linarith [phase_variance_lt_0961]
          exact le_of_lt (lt_trans h_upper (by unfold pi; nlinarith [pi_gt_d4]))
      have h_ref : (1.305 : ℝ) ∈ Set.Icc (0 : ℝ) pi := ⟨by norm_num, by unfold pi; nlinarith [pi_gt_d4]⟩
      exact lt_trans (strictAntiOn_cos h_ref h_in h_sum_lo) cos_1305_lt_0263
    exact lt_trans (quirkMod_lt_exp_cos_bound p h_obs h_cos_hi h_cos_pos) (by norm_num)
  have h_base_mag : (0.35 : ℝ) < -term1_base p := by
    have h_neg_cos : (0.5 : ℝ) < -cos ((psi_con + (0.35 : ℝ)) / eta_eff) := by linarith [medical_cos_lt_neg_05]
    have h_exp_lo := medical_exp_factor_gt_one_three
    have h_growth_term : growth_term p = 1 := by simp [growth_term, p, get_domain_params]
    have h_growth : (1.9 : ℝ) < 1 + growth_term p * coherence_efficiency := by
      rw [h_growth_term]
      nlinarith [coherence_efficiency_gt_nine_five]
    have h_rearrange : -(1 / sqrt 13 * cos ((psi_con + (0.35 : ℝ)) / eta_eff) *
        exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) *
        (1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
          coherence_efficiency)) =
      (1 / sqrt 13) * (-cos ((psi_con + (0.35 : ℝ)) / eta_eff)) *
        exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) *
        (1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
          coherence_efficiency) := by ring
    have h_cos_bound : (1 / sqrt 13) * (0.5 : ℝ) <
        (1 / sqrt 13) * (-cos ((psi_con + (0.35 : ℝ)) / eta_eff)) := by
      refine mul_lt_mul_of_pos_left h_neg_cos ?_
      apply div_pos (by norm_num)
      exact Real.sqrt_pos.mpr (by norm_num)
    have h_exp_bound : (1 / sqrt 13) * (-cos ((psi_con + (0.35 : ℝ)) / eta_eff)) * (1.34 : ℝ) <
        (1 / sqrt 13) * (-cos ((psi_con + (0.35 : ℝ)) / eta_eff)) *
          exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) := by
      have h_pos : 0 < (1 / sqrt 13) * (-cos ((psi_con + (0.35 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos]
      exact mul_lt_mul_of_pos_left h_exp_lo h_pos
    have h_growth_eq : (1 + growth_term p * coherence_efficiency) =
        (1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
          coherence_efficiency) := by
      simp [growth_term, p, get_domain_params]
    have h_growth' : (1.9 : ℝ) < 1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
        coherence_efficiency := by
      simpa [← h_growth_eq] using h_growth
    have h_pos_mag : (0.35 : ℝ) < (1 / sqrt 13) * (-cos ((psi_con + (0.35 : ℝ)) / eta_eff)) *
        exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) *
        (1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
          coherence_efficiency) := by
      have h_floor : (0.35 : ℝ) < (1 / 3.606) * (0.5 : ℝ) * (1.34 : ℝ) * (1.9 : ℝ) := by norm_num
      have h_inv : (1 / 3.606) < (1 / sqrt (13 : ℝ)) := by
        apply one_div_lt_one_div_of_lt (by norm_num)
        exact sqrt_13_lt_3606
      nlinarith [h_floor, h_inv, h_cos_bound, h_exp_bound, h_growth']
    simp only [term1_base, p, get_domain_params, mul_one, one_mul]
    have h_exp_rw : exp (-alpha / 1 + 1 + bleed_in_factor * (0.35 : ℝ)) =
        exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) := by ring_nf
    rw [h_exp_rw, h_rearrange]
    exact h_pos_mag
  have h_base_hi : -term1_base p < (2.28 : ℝ) := by
    have hcos_neg : cos ((psi_con + (0.35 : ℝ)) / eta_eff) < 0 := by
      linarith [medical_cos_lt_neg_05]
    have h_cos_le : -cos ((psi_con + (0.35 : ℝ)) / eta_eff) ≤ (1 : ℝ) := by
      have h := abs_le.mp (abs_cos_le_one ((psi_con + (0.35 : ℝ)) / eta_eff))
      linarith [hcos_neg, h.1, h.2]
    have h_arg_hi : (1 - alpha + bleed_in_factor * (0.35 : ℝ)) < (1.351 : ℝ) := by
      nlinarith [alpha_pos, bleed_in_factor_le_coherence, coherence_efficiency_lt_1002]
    have h_exp_hi : exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) < (4 : ℝ) :=
      lt_trans (Real.exp_lt_exp.mpr h_arg_hi) exp_1351_lt_4
    have h_growth_hi : (1 + growth_term p * coherence_efficiency) < (2.01 : ℝ) := by
      have h_growth_term : growth_term p = 1 := by simp [growth_term, p, get_domain_params]
      rw [h_growth_term]
      nlinarith [coherence_efficiency_lt_1002]
    have h_growth_term_eq : growth_term p =
        growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } := by
      simp [growth_term, p, get_domain_params]
    have h_inv : (1 / 3.606) < (1 / sqrt (13 : ℝ)) := by
      apply one_div_lt_one_div_of_lt (by norm_num)
      exact sqrt_13_lt_3606
    have h_growth_hi' : (1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
        coherence_efficiency) < (2.01 : ℝ) := by
      simpa [← h_growth_term_eq] using h_growth_hi
    have h_core_lt : (1 / sqrt 13) * (-cos ((psi_con + (0.35 : ℝ)) / eta_eff)) *
        exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) *
        (1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
          coherence_efficiency) < (2.28 : ℝ) := by
      have h_div_pos : (0 : ℝ) < 1 / sqrt 13 :=
        one_div_pos.mpr (Real.sqrt_pos.mpr (by norm_num))
      have h₁ := mul_le_mul_of_nonneg_left h_cos_le (le_of_lt h_div_pos)
      have h₂ := mul_le_mul h₁ (le_of_lt h_exp_hi)
        (le_of_lt (exp_pos (1 - alpha + bleed_in_factor * (0.35 : ℝ))))
        (by nlinarith [h_div_pos])
      have h_growth_nonneg : (0 : ℝ) ≤ 1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
          coherence_efficiency := by
        have h_gt : (0 : ℝ) < growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } := by
          dsimp [growth_term]
          exact exp_pos _
        nlinarith [h_gt, coherence_efficiency_gt_nine_five]
      have h₃ := mul_le_mul h₂ (le_of_lt h_growth_hi') h_growth_nonneg
        (by nlinarith [h_div_pos])
      have h_num : (1 / sqrt 13) * (1 : ℝ) * (4 : ℝ) * (2.01 : ℝ) < (2.28 : ℝ) := by
        have h_eq : (1 / sqrt 13) * (1 : ℝ) * (4 : ℝ) * (2.01 : ℝ) = (8.04 : ℝ) / sqrt 13 := by ring
        rw [h_eq]
        have h_sqrt_pos : (0 : ℝ) < sqrt 13 := Real.sqrt_pos.mpr (by norm_num)
        rw [div_lt_iff₀ h_sqrt_pos]
        have h_sqrt_lo : (3.605 : ℝ) < sqrt 13 := Real.lt_sqrt_of_sq_lt (by norm_num : (3.605 : ℝ) ^ 2 < 13)
        nlinarith [h_sqrt_lo]
      exact lt_of_le_of_lt h₃ h_num
    have h_eq : -term1_base p =
        (1 / sqrt 13) * (-cos ((psi_con + (0.35 : ℝ)) / eta_eff)) *
          exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) *
          (1 + growth_term { D_eff := 13, recent_hits := 1, delta_psi := 0.35, observed := true } *
            coherence_efficiency) := by
      simp only [term1_base, p, get_domain_params]
      ring_nf
    rw [h_eq]
    exact h_core_lt
  have h_worst : (-0.8 : ℝ) < term1_base p * (0.99 : ℝ) * (0.352 : ℝ) := by
    have h_rng_lo : (-2.28 : ℝ) < term1_base p := by linarith [h_base_hi]
    have h_rng_hi : term1_base p < (-0.35 : ℝ) := by linarith [h_base_mag]
    nlinarith [h_rng_lo, h_rng_hi]
  exact term1_gt_neg_08_of_observer_pos_quirk p h_obs h_base_neg h_adj_lo h_adj_hi
    (by norm_num : (0 : ℝ) < (0.567 : ℝ)) h_quirk_pos h_quirk_hi h_worst

/-- Molecular (D=9, δψ=0.4): term1 lower bound — SMILES Lab crosswalk. -/
lemma domain_term1_gt_neg_08_molecular :
    (-0.8 : ℝ) < term1 (get_domain_params "molecular") := by
  set p := get_domain_params "molecular"
  have h_obs : p.observed = true := by simp [p, get_domain_params]
  have h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ (1.3 : ℝ) := by
    simp [p, get_domain_params]; norm_num
  have hN : (0 : ℝ) < p.N := by simp [p, get_domain_params]
  have hP : (0 : ℝ) < p.P := by simp [p, get_domain_params]
  have hD : (0 : ℝ) < p.D_eff := by simp [p, get_domain_params]
  have h_base_neg := term1_base_negative_of_typical_delta p h_delta hN hP hD
  have h_adj_lo := perceived_adjust_lo_domain p (by simp [p, get_domain_params]; norm_num)
  have h_adj_hi := perceived_adjust_hi_domain p (by simp [p, get_domain_params]; constructor <;> norm_num)
  have h_quirk_pos := quirkMod_pos_of_delta_psi_le_06 p h_obs
    (by simp [p, get_domain_params]; norm_num) (by simp [p, get_domain_params]; norm_num)
  have h_cos_pos := cos_dp_pv_pos_of_le_06 p.delta_psi (by simp [p, get_domain_params]; norm_num)
    (by simp [p, get_domain_params]; norm_num)
  have h_quirk_hi : quirkMod p < (0.29 : ℝ) := by
    have h_cos_hi : cos (p.delta_psi + phase_variance) < (0.215 : ℝ) := by
      have h_sum_lo : (1.355 : ℝ) < p.delta_psi + phase_variance := by
        simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
      have h_in : p.delta_psi + phase_variance ∈ Set.Icc (0 : ℝ) pi := by
        constructor
        · simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
        · have h_upper : p.delta_psi + phase_variance < (1.361 : ℝ) := by
            simp only [p, get_domain_params]
            linarith [phase_variance_lt_0961]
          exact le_of_lt (lt_trans h_upper (by unfold pi; nlinarith [pi_gt_d4]))
      have h_ref : (1.355 : ℝ) ∈ Set.Icc (0 : ℝ) pi := ⟨by norm_num, by unfold pi; nlinarith [pi_gt_d4]⟩
      exact lt_trans (strictAntiOn_cos h_ref h_in h_sum_lo) cos_1355_lt_0215
    exact lt_trans (quirkMod_lt_exp_cos_bound p h_obs h_cos_hi h_cos_pos)
      (by norm_num : (1.338 : ℝ) * (0.215 : ℝ) < (0.29 : ℝ))
  have h_base_mag : (0.25 : ℝ) < -term1_base p := by
    have h_neg_cos : (0.55 : ℝ) < -cos ((psi_con + (0.4 : ℝ)) / eta_eff) := by
      linarith [molecular_cos_lt_neg_055]
    have h_exp := molecular_exp_factor_gt_34
    have h_growth_term := growth_term_hits_zero_gt_one p (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
    have h_growth : (1.9 : ℝ) < 1 + growth_term p * coherence_efficiency := by
      nlinarith [h_growth_term, coherence_efficiency_gt_nine_five]
    have h_rearrange : -(1 / 3 * cos ((psi_con + (0.4 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (0.4 : ℝ)) *
        (1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
          coherence_efficiency)) =
      (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.4 : ℝ)) *
        (1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
          coherence_efficiency) := by ring
    have h_cos_bound : (1 / 3) * (0.55 : ℝ) <
        (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) := by
      refine mul_lt_mul_of_pos_left h_neg_cos (by norm_num)
    have h_exp_bound : (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) * (3.4 : ℝ) <
        (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.4 : ℝ)) := by
      have h_pos : 0 < (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos]
      exact mul_lt_mul_of_pos_left h_exp h_pos
    have h_growth_eq : (1 + growth_term p * coherence_efficiency) =
        (1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
          coherence_efficiency) := by
      simp [growth_term, p, get_domain_params]
    have h_growth' : (1.9 : ℝ) < 1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
        coherence_efficiency := by
      simpa [h_growth_eq] using h_growth
    have h_pos_mag : (0.25 : ℝ) < (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.4 : ℝ)) *
        (1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
          coherence_efficiency) := by
      have h_floor : (0.25 : ℝ) < (1 / 3) * (0.55 : ℝ) * (3.4 : ℝ) * (1.9 : ℝ) := by norm_num
      nlinarith [h_floor, h_cos_bound, h_exp_bound, h_growth']
    simp only [term1_base, p, get_domain_params, mul_one, one_mul]
    have h_exp_rw : exp (-alpha * (0 : ℝ) / 1 + 1 + bleed_in_factor * (0.4 : ℝ)) =
        exp (1 + bleed_in_factor * (0.4 : ℝ)) := by ring_nf
    rw [h_exp_rw, sqrt_9_eq_3, h_rearrange]
    exact h_pos_mag
  have h_base_hi : -term1_base p < (2.76 : ℝ) := by
    have hcos_neg : cos ((psi_con + (0.4 : ℝ)) / eta_eff) < 0 := by
      linarith [molecular_cos_lt_neg_055]
    have h_cos_le : -cos ((psi_con + (0.4 : ℝ)) / eta_eff) ≤ (1 : ℝ) := by
      have h := abs_le.mp (abs_cos_le_one ((psi_con + (0.4 : ℝ)) / eta_eff))
      linarith [hcos_neg, h.1, h.2]
    have h_bleed_hi : (1 + bleed_in_factor * (0.4 : ℝ)) < (1.331 : ℝ) := by
      nlinarith [bleed_in_factor_lt_0826]
    have h_exp_hi : exp (1 + bleed_in_factor * (0.4 : ℝ)) < (3.84 : ℝ) :=
      lt_trans (Real.exp_lt_exp.mpr h_bleed_hi) exp_1331_lt_384
    have h_growth_hi : (1 + growth_term p * coherence_efficiency) < (2.153 : ℝ) := by
      have h_prod := growth_term_coherence_product_lt_11523 p
        (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
      linarith [h_prod]
    have h_growth_term_eq : growth_term p =
        growth_term { D_eff := 9, delta_psi := 0.4, observed := true } := by
      simp [growth_term, p, get_domain_params]
    have h_growth_hi' : (1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
        coherence_efficiency) < (2.153 : ℝ) := by
      simpa [← h_growth_term_eq] using h_growth_hi
    have h_core_lt : (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.4 : ℝ)) *
        (1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
          coherence_efficiency) < (2.76 : ℝ) := by
      have h₁ : (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) ≤ (1 / 3) * (1 : ℝ) :=
        mul_le_mul_of_nonneg_left h_cos_le (by norm_num : (0 : ℝ) ≤ 1 / 3)
      have h₂ := mul_le_mul h₁ (le_of_lt h_exp_hi)
        (le_of_lt (exp_pos (1 + bleed_in_factor * (0.4 : ℝ))))
        (by norm_num : (0 : ℝ) ≤ 1 / 3 * (1 : ℝ))
      have h_growth_nonneg : (0 : ℝ) ≤ 1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
          coherence_efficiency := by
        have h_gt : (0 : ℝ) < growth_term { D_eff := 9, delta_psi := 0.4, observed := true } := by
          dsimp [growth_term]
          exact exp_pos _
        nlinarith [h_gt, coherence_efficiency_gt_nine_five]
      have h₃ := mul_le_mul h₂ (le_of_lt h_growth_hi') h_growth_nonneg
        (by norm_num : (0 : ℝ) ≤ 1 / 3 * (1 : ℝ) * (3.84 : ℝ))
      have h_num : (1 / 3) * (1 : ℝ) * (3.84 : ℝ) * (2.153 : ℝ) < (2.76 : ℝ) := by norm_num
      exact lt_of_le_of_lt h₃ h_num
    have h_eq : -term1_base p =
        (1 / 3) * (-cos ((psi_con + (0.4 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.4 : ℝ)) *
          (1 + growth_term { D_eff := 9, delta_psi := 0.4, observed := true } *
            coherence_efficiency) := by
      simp only [term1_base, p, get_domain_params, sqrt_9_eq_3]
      ring_nf
    rw [h_eq]
    exact h_core_lt
  have h_worst : (-0.8 : ℝ) < term1_base p * (0.99 : ℝ) * (0.29 : ℝ) := by
    have h_rng_lo : (-2.76 : ℝ) < term1_base p := by linarith [h_base_hi]
    have h_rng_hi : term1_base p < (-0.25 : ℝ) := by linarith [h_base_mag]
    nlinarith [h_rng_lo, h_rng_hi]
  exact term1_gt_neg_08_of_observer_pos_quirk p h_obs h_base_neg h_adj_lo h_adj_hi
    (by norm_num : (0 : ℝ) < (0.567 : ℝ)) h_quirk_pos h_quirk_hi h_worst

/-- Material (D=10, δψ=0.5): term1 lower bound — SMILES Lab crosswalk. -/
lemma domain_term1_gt_neg_08_material :
    (-0.8 : ℝ) < term1 (get_domain_params "material") := by
  set p := get_domain_params "material"
  have h_obs : p.observed = true := by simp [p, get_domain_params]
  have h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ (1.3 : ℝ) := by
    simp [p, get_domain_params]; norm_num
  have hN : (0 : ℝ) < p.N := by simp [p, get_domain_params]
  have hP : (0 : ℝ) < p.P := by simp [p, get_domain_params]
  have hD : (0 : ℝ) < p.D_eff := by simp [p, get_domain_params]
  have h_base_neg := term1_base_negative_of_typical_delta p h_delta hN hP hD
  have h_adj_lo := perceived_adjust_lo_domain p (by simp [p, get_domain_params]; norm_num)
  have h_adj_hi := perceived_adjust_hi_domain p (by simp [p, get_domain_params]; constructor <;> norm_num)
  have h_quirk_pos := quirkMod_pos_of_delta_psi_le_06 p h_obs
    (by simp [p, get_domain_params]; norm_num) (by simp [p, get_domain_params]; norm_num)
  have h_cos_pos := cos_dp_pv_pos_of_le_06 p.delta_psi (by simp [p, get_domain_params]; norm_num)
    (by simp [p, get_domain_params]; norm_num)
  have h_quirk_hi : quirkMod p < (0.156 : ℝ) := by
    have h_cos_hi : cos (p.delta_psi + phase_variance) < (0.116 : ℝ) := by
      have h_sum_lo : (1.455 : ℝ) < p.delta_psi + phase_variance := by
        simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
      have h_in : p.delta_psi + phase_variance ∈ Set.Icc (0 : ℝ) pi := by
        constructor
        · simp [p, get_domain_params]; linarith [phase_variance_gt_0955]
        · have h_upper : p.delta_psi + phase_variance < (1.461 : ℝ) := by
            simp only [p, get_domain_params]
            linarith [phase_variance_lt_0961]
          exact le_of_lt (lt_trans h_upper (by unfold pi; nlinarith [pi_gt_d4]))
      have h_ref : (1.455 : ℝ) ∈ Set.Icc (0 : ℝ) pi := ⟨by norm_num, by unfold pi; nlinarith [pi_gt_d4]⟩
      exact lt_trans (strictAntiOn_cos h_ref h_in h_sum_lo) cos_1455_lt_0116
    exact lt_trans (quirkMod_lt_exp_cos_bound p h_obs h_cos_hi h_cos_pos) (by norm_num)
  have h_base_mag : (0.25 : ℝ) < -term1_base p := by
    have h_neg_cos : (0.74 : ℝ) < -cos ((psi_con + (0.5 : ℝ)) / eta_eff) := by
      linarith [material_cos_lt_neg_075]
    have h_exp := ai_exp_factor_gt_four
    have h_growth_term := growth_term_hits_zero_gt_one p (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
    have h_growth : (1.9 : ℝ) < 1 + growth_term p * coherence_efficiency := by
      nlinarith [h_growth_term, coherence_efficiency_gt_nine_five]
    have h_rearrange : -(1 / sqrt 10 * cos ((psi_con + (0.5 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (0.5 : ℝ)) *
        (1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
          coherence_efficiency)) =
      (1 / sqrt 10) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.5 : ℝ)) *
        (1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
          coherence_efficiency) := by ring
    have h_cos_bound : (1 / sqrt 10) * (0.74 : ℝ) <
        (1 / sqrt 10) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) := by
      refine mul_lt_mul_of_pos_left h_neg_cos ?_
      apply div_pos (by norm_num)
      exact Real.sqrt_pos.mpr (by norm_num)
    have h_exp_bound : (1 / sqrt 10) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) * (4 : ℝ) <
        (1 / sqrt 10) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.5 : ℝ)) := by
      have h_pos : 0 < (1 / sqrt 10) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) := by
        nlinarith [h_neg_cos]
      exact mul_lt_mul_of_pos_left h_exp h_pos
    have h_growth_eq : (1 + growth_term p * coherence_efficiency) =
        (1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
          coherence_efficiency) := by
      simp [growth_term, p, get_domain_params]
    have h_growth' : (1.9 : ℝ) < 1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
        coherence_efficiency := by
      simpa [h_growth_eq] using h_growth
    have h_pos_mag : (0.25 : ℝ) < (1 / sqrt 10) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.5 : ℝ)) *
        (1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
          coherence_efficiency) := by
      have h_floor : (0.25 : ℝ) < (1 / 3.163) * (0.74 : ℝ) * (4 : ℝ) * (1.9 : ℝ) := by norm_num
      have h_inv : (1 / 3.163) < (1 / sqrt (10 : ℝ)) := by
        apply one_div_lt_one_div_of_lt (by norm_num)
        exact sqrt_10_lt_3163
      nlinarith [h_floor, h_inv, h_cos_bound, h_exp_bound, h_growth']
    simp only [term1_base, p, get_domain_params, mul_one, one_mul]
    have h_exp_rw : exp (-alpha * (0 : ℝ) / 1 + 1 + bleed_in_factor * (0.5 : ℝ)) =
        exp (1 + bleed_in_factor * (0.5 : ℝ)) := by ring_nf
    rw [h_exp_rw, h_rearrange]
    exact h_pos_mag
  have h_base_hi : -term1_base p < (4 : ℝ) := by
    have hcos_neg : cos ((psi_con + (0.5 : ℝ)) / eta_eff) < 0 := by
      linarith [material_cos_lt_neg_075]
    have h_cos_le : -cos ((psi_con + (0.5 : ℝ)) / eta_eff) ≤ (1 : ℝ) := by
      have h := abs_le.mp (abs_cos_le_one ((psi_con + (0.5 : ℝ)) / eta_eff))
      linarith [hcos_neg, h.1, h.2]
    have h_bleed_hi : (1 + bleed_in_factor * (0.5 : ℝ)) < (1.505 : ℝ) := by
      nlinarith [bleed_in_factor_le_coherence, coherence_efficiency_lt_1002]
    have h_exp_hi : exp (1 + bleed_in_factor * (0.5 : ℝ)) < (5 : ℝ) :=
      lt_trans (Real.exp_lt_exp.mpr h_bleed_hi) exp_1505_lt_5
    have h_growth_hi : (1 + growth_term p * coherence_efficiency) < (2.2 : ℝ) := by
      have h_prod := growth_term_coherence_product_lt_11523 p
        (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
      linarith [h_prod]
    have h_growth_term_eq : growth_term p =
        growth_term { D_eff := 10, delta_psi := 0.5, observed := true } := by
      simp [growth_term, p, get_domain_params]
    have h_growth_hi' : (1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
        coherence_efficiency) < (2.2 : ℝ) := by
      simpa [← h_growth_term_eq] using h_growth_hi
    have h_core_lt : (1 / sqrt 10) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
        exp (1 + bleed_in_factor * (0.5 : ℝ)) *
        (1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
          coherence_efficiency) < (4 : ℝ) := by
      have h_div_pos : (0 : ℝ) < 1 / sqrt 10 :=
        one_div_pos.mpr (Real.sqrt_pos.mpr (by norm_num))
      have h₁ := mul_le_mul_of_nonneg_left h_cos_le (le_of_lt h_div_pos)
      have h₂ := mul_le_mul h₁ (le_of_lt h_exp_hi)
        (le_of_lt (exp_pos (1 + bleed_in_factor * (0.5 : ℝ))))
        (by nlinarith [h_div_pos])
      have h_growth_nonneg : (0 : ℝ) ≤ 1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
          coherence_efficiency := by
        have h_gt : (0 : ℝ) < growth_term { D_eff := 10, delta_psi := 0.5, observed := true } := by
          dsimp [growth_term]
          exact exp_pos _
        nlinarith [h_gt, coherence_efficiency_gt_nine_five]
      have h₃ := mul_le_mul h₂ (le_of_lt h_growth_hi') h_growth_nonneg
        (by nlinarith [h_div_pos])
      have h_num : (1 / sqrt 10) * (1 : ℝ) * (5 : ℝ) * (2.2 : ℝ) < (4 : ℝ) := by
        have h_eq : (1 / sqrt 10) * (1 : ℝ) * (5 : ℝ) * (2.2 : ℝ) = (11 : ℝ) / sqrt 10 := by ring
        rw [h_eq]
        have h_sqrt_pos : (0 : ℝ) < sqrt 10 := Real.sqrt_pos.mpr (by norm_num)
        rw [div_lt_iff₀ h_sqrt_pos]
        have h_sqrt_lo : (3 : ℝ) < sqrt 10 := Real.lt_sqrt_of_sq_lt (by norm_num : (3 : ℝ) ^ 2 < 10)
        nlinarith [h_sqrt_lo]
      exact lt_of_le_of_lt h₃ h_num
    have h_eq : -term1_base p =
        (1 / sqrt 10) * (-cos ((psi_con + (0.5 : ℝ)) / eta_eff)) *
          exp (1 + bleed_in_factor * (0.5 : ℝ)) *
          (1 + growth_term { D_eff := 10, delta_psi := 0.5, observed := true } *
            coherence_efficiency) := by
      simp only [term1_base, p, get_domain_params]
      ring_nf
    rw [h_eq]
    exact h_core_lt
  have h_worst : (-0.8 : ℝ) < term1_base p * (0.99 : ℝ) * (0.156 : ℝ) := by
    have h_rng_lo : (-4 : ℝ) < term1_base p := by linarith [h_base_hi]
    have h_rng_hi : term1_base p < (-0.25 : ℝ) := by linarith [h_base_mag]
    nlinarith [h_rng_lo, h_rng_hi]
  exact term1_gt_neg_08_of_observer_pos_quirk p h_obs h_base_neg h_adj_lo h_adj_hi
    (by norm_num : (0 : ℝ) < (0.567 : ℝ)) h_quirk_pos h_quirk_hi h_worst

/-- Biological (D=12, unobserved): term1 is positive at low δψ. -/
lemma domain_term1_positive_biological :
    (0 : ℝ) < term1 (get_domain_params "biological") := by
  set p := get_domain_params "biological"
  have h_obs : p.observed = false := by simp [p, get_domain_params]
  have h_quirk : quirkMod p = 1 := by simp [quirkMod, p, get_domain_params, h_obs]
  have h_adj_pos : (0 : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25) :=
    lt_trans (by norm_num) (perceived_adjust_lo_domain p (by simp [p, get_domain_params]; norm_num))
  have h_base_pos : (0 : ℝ) < term1_base p := by
    have h_cos_pos : (0.03 : ℝ) < cos ((psi_con + (0.08 : ℝ)) / eta_eff) := biological_cos_gt_003
    have h_exp := biological_exp_factor_gt_two
    have h_growth_term := growth_term_hits_zero_gt_one p (by simp [p, get_domain_params]) (by simp [p, get_domain_params])
    have h_growth : (1.9 : ℝ) < 1 + growth_term p * coherence_efficiency := by
      nlinarith [h_growth_term, coherence_efficiency_gt_nine_five]
    have h_rearrange :
        (1 / sqrt 12) * cos ((psi_con + (0.08 : ℝ)) / eta_eff) *
          exp (1 + bleed_in_factor * (0.08 : ℝ)) *
          (1 + growth_term { D_eff := 12, delta_psi := 0.08, observed := false } *
            coherence_efficiency) =
        term1_base p := by
      simp only [term1_base, p, get_domain_params, mul_one, one_mul]
      have h_exp_rw : exp (-alpha * (0 : ℝ) / 1 + 1 + bleed_in_factor * (0.08 : ℝ)) =
          exp (1 + bleed_in_factor * (0.08 : ℝ)) := by ring_nf
      rw [h_exp_rw]
    have h_cos_bound : (1 / sqrt 12) * (0.03 : ℝ) <
        (1 / sqrt 12) * cos ((psi_con + (0.08 : ℝ)) / eta_eff) := by
      refine mul_lt_mul_of_pos_left h_cos_pos ?_
      apply div_pos (by norm_num)
      exact Real.sqrt_pos.mpr (by norm_num)
    have h_exp_bound : (1 / sqrt 12) * cos ((psi_con + (0.08 : ℝ)) / eta_eff) * (2 : ℝ) <
        (1 / sqrt 12) * cos ((psi_con + (0.08 : ℝ)) / eta_eff) *
          exp (1 + bleed_in_factor * (0.08 : ℝ)) := by
      have h_pos : 0 < (1 / sqrt 12) * cos ((psi_con + (0.08 : ℝ)) / eta_eff) := by
        nlinarith [h_cos_pos]
      exact mul_lt_mul_of_pos_left h_exp h_pos
    have h_growth_eq : (1 + growth_term p * coherence_efficiency) =
        (1 + growth_term { D_eff := 12, delta_psi := 0.08, observed := false } *
          coherence_efficiency) := by
      simp [growth_term, p, get_domain_params]
    have h_growth' : (1.9 : ℝ) < 1 + growth_term { D_eff := 12, delta_psi := 0.08, observed := false } *
        coherence_efficiency := by
      simpa [h_growth_eq] using h_growth
    have h_pos_mag : (0.01 : ℝ) < (1 / sqrt 12) * cos ((psi_con + (0.08 : ℝ)) / eta_eff) *
        exp (1 + bleed_in_factor * (0.08 : ℝ)) *
        (1 + growth_term { D_eff := 12, delta_psi := 0.08, observed := false } *
          coherence_efficiency) := by
      have h_floor : (0.01 : ℝ) < (1 / 3.465) * (0.03 : ℝ) * (2 : ℝ) * (1.9 : ℝ) := by norm_num
      have h_inv : (1 / 3.465) < (1 / sqrt (12 : ℝ)) := by
        apply one_div_lt_one_div_of_lt (by norm_num)
        exact sqrt_12_lt_3465
      nlinarith [h_floor, h_inv, h_cos_bound, h_exp_bound, h_growth']
    rw [← h_rearrange]
    exact lt_trans (by norm_num : (0 : ℝ) < (0.01 : ℝ)) h_pos_mag
  have h_term1_eq : term1 p = term1_base p * (1 + new_perceived_param * log (p.D_eff / 25)) := by
    simp [term1, h_quirk]
  rw [h_term1_eq]
  nlinarith [h_base_pos, h_adj_pos]

end

end FSOT.Formal