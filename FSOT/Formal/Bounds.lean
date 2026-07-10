/-
  Numeric interval bounds for FSOT.Formal constants.
-/

import FSOT.Formal.Scalar
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Monotone
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Algebra.Order.GroupWithZero.Basic
import Mathlib.Tactic.Linarith

namespace FSOT.Formal

noncomputable section

open Real

lemma gamma_euler_pos : (0 : ℝ) < gamma_euler := by unfold gamma_euler; norm_num

lemma phi_gt_one : (1 : ℝ) < phi := by
  unfold phi
  have h_sqrt5 : (2 : ℝ) < sqrt 5 := lt_sqrt_of_sq_lt (by norm_num)
  linarith [h_sqrt5]

lemma phi_lt_two : phi < (2 : ℝ) := by
  unfold phi
  have h_sqrt5 : sqrt 5 < (2.24 : ℝ) := by
    have h := Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 5) (by norm_num : (5 : ℝ) < (2.24 : ℝ) ^ 2)
    simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ (2.24 : ℝ))] using h
  linarith [h_sqrt5]

lemma phi_gt_1618 : (1.618 : ℝ) < phi := by
  unfold phi
  have h : (2.236 : ℝ) < sqrt 5 := Real.lt_sqrt_of_sq_lt (by norm_num : (2.236 : ℝ) ^ 2 < 5)
  linarith [h]

lemma phi_lt_16181 : phi < (1.6181 : ℝ) := by
  unfold phi
  have h_s : sqrt 5 < (2.2361 : ℝ) := by
    have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (5 : ℝ) < (2.2361 : ℝ) ^ 2)
    simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 2.2361)] using h
  linarith [h_s]

lemma pi_eq_real_pi : pi = π := rfl

lemma pi_gt_one : (1 : ℝ) < pi := by
  unfold pi
  exact lt_trans (by norm_num) pi_gt_d4

lemma pi_sub_one_pos : (0 : ℝ) < pi - 1 := sub_pos.mpr pi_gt_one

lemma eta_pos : (0 : ℝ) < eta_eff := by
  unfold eta_eff
  exact div_pos (by norm_num) pi_sub_one_pos

lemma exp_neg_one_gt_367 : (0.367 : ℝ) < exp (-1) := by
  rw [exp_neg]
  have h : exp 1 < (1 / 0.367 : ℝ) := lt_trans exp_one_lt_d9 (by norm_num)
  simpa [one_div_one_div] using one_div_lt_one_div_of_lt (exp_pos _) h

lemma exp_neg_one_lt_368 : exp (-1) < (0.368 : ℝ) := by
  rw [exp_neg]
  have h : (1 / 0.368 : ℝ) < exp 1 := lt_trans (by norm_num) exp_one_gt_d9
  simpa [one_div_one_div] using one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < 1 / 0.368) h

lemma psi_con_gt_632 : (0.632 : ℝ) < psi_con := by
  unfold psi_con; linarith [exp_neg_one_lt_368]

lemma psi_con_lt_633 : psi_con < (0.633 : ℝ) := by
  unfold psi_con; linarith [exp_neg_one_gt_367]

lemma eta_eff_gt_466 : (0.466 : ℝ) < eta_eff := by
  unfold eta_eff
  have hpi : pi < (3.1416 : ℝ) := by unfold pi; exact pi_lt_d4
  have h_sub : pi - 1 < (2.1416 : ℝ) := by linarith
  have h := one_div_lt_one_div_of_lt pi_sub_one_pos h_sub
  have h_num : (1 / (2.1416 : ℝ)) < eta_eff := by simpa [eta_eff] using h
  linarith

lemma eta_eff_lt_467 : eta_eff < (0.467 : ℝ) := by
  unfold eta_eff
  have hpi : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
  have h_sub : (2.1415 : ℝ) < pi - 1 := by linarith
  have h := one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < 2.1415) h_sub
  have h_num : eta_eff < (1 / (2.1415 : ℝ)) := by simpa [eta_eff] using h
  linarith

lemma cos_arg_gt_pi_div_two
    (p : FSOTParams)
    (h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3) :
    pi / 2 < (psi_con + p.delta_psi) / eta_eff := by
  have h_num_lo : (0.982 : ℝ) < psi_con + p.delta_psi := by linarith [psi_con_gt_632, h_delta.1]
  have h_div : (0.982 : ℝ) / eta_eff < (psi_con + p.delta_psi) / eta_eff :=
    div_lt_div_of_pos_right h_num_lo eta_pos
  have h_eta_hi : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
  have h_lo : (0.982 : ℝ) / (0.467 : ℝ) < (0.982 : ℝ) / eta_eff := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
    exact h_eta_hi
  have h_pi : pi / 2 < (0.982 : ℝ) / (0.467 : ℝ) := by
    have h1 : pi / 2 < (1.571 : ℝ) := by unfold pi; nlinarith [pi_lt_d4]
    have h2 : (1.571 : ℝ) < (0.982 : ℝ) / (0.467 : ℝ) := by norm_num
    linarith
  linarith [h_div, h_lo, h_pi]

lemma cos_arg_lt_three_pi_div_two
    (p : FSOTParams)
    (h_delta : (0.35 : ℝ) ≤ p.delta_psi ∧ p.delta_psi ≤ 1.3) :
    (psi_con + p.delta_psi) / eta_eff < pi + pi / 2 := by
  have h_num_hi : psi_con + p.delta_psi < (1.933 : ℝ) := by linarith [psi_con_lt_633, h_delta.2]
  have h_div : (psi_con + p.delta_psi) / eta_eff < (1.933 : ℝ) / eta_eff :=
    div_lt_div_of_pos_right h_num_hi eta_pos
  have h_eta_lo : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_hi : (1.933 : ℝ) / eta_eff < (1.933 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta_lo
  have h_pi : (1.933 : ℝ) / (0.466 : ℝ) < pi + pi / 2 := by
    have h_mid : (1.933 : ℝ) / (0.466 : ℝ) < (4.15 : ℝ) := by norm_num
    have h_upper : (4.15 : ℝ) < pi + pi / 2 := by unfold pi; nlinarith [pi_gt_d4]
    linarith
  linarith [h_div, h_hi, h_pi]

lemma exp_neg_0298_lt_08 : exp (-0.298) < (0.8 : ℝ) := by
  have h := add_one_lt_exp (by norm_num : (0.298 : ℝ) ≠ 0)
  have h' : (1 / 0.8 : ℝ) < exp 0.298 := by linarith
  have h'' := (one_div_lt (exp_pos _) (by norm_num : (0 : ℝ) < 0.8)).mpr h'
  simpa [exp_neg] using h''

lemma log_08_gt_m0298 : (-0.298 : ℝ) < log (0.8 : ℝ) :=
  (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 0.8)).2 exp_neg_0298_lt_08

lemma exp_03_gt_12 : (1.2 : ℝ) < exp 0.3 := by
  have h := add_one_lt_exp (by norm_num : (0.3 : ℝ) ≠ 0)
  linarith

lemma log_12_lt : log (1.2 : ℝ) < (0.3 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 1.2)).2 exp_03_gt_12

lemma sqrt_two_lt_14142135624 : sqrt 2 < (1.4142135624 : ℝ) := by
  have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (2 : ℝ) < (1.4142135624 : ℝ) ^ 2)
  simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 1.4142135624)] using h

lemma new_perceived_param_lt_031 : new_perceived_param < (0.301 : ℝ) := by
  have h_exact : (0.578 : ℝ) / (2.7182818283 : ℝ) * (1.4142135624 : ℝ) < (0.301 : ℝ) := by norm_num
  unfold new_perceived_param gamma_euler e sqrt2
  have hγ_pos : (0 : ℝ) < gamma_euler / (2.7182818283 : ℝ) := div_pos gamma_euler_pos (by norm_num)
  have hsqrt_pos : (0 : ℝ) < sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have hdiv_core : gamma_euler / exp 1 < gamma_euler / (2.7182818283 : ℝ) :=
    div_lt_div_of_pos_left gamma_euler_pos (by norm_num) exp_one_gt_d9
  have hdiv := mul_lt_mul_of_pos_right hdiv_core hsqrt_pos
  have hsqrt := mul_lt_mul_of_pos_left sqrt_two_lt_14142135624 hγ_pos
  have hγ := mul_lt_mul_of_pos_right
    (div_lt_div_of_pos_right
      (by norm_num : (0.57721566490153286060651209008240243 : ℝ) < (0.578 : ℝ))
      (by norm_num : (0 : ℝ) < (2.7182818283 : ℝ)))
    (by norm_num : (0 : ℝ) < (1.4142135624 : ℝ))
  exact lt_trans hdiv (lt_trans hsqrt (lt_trans hγ h_exact))

lemma new_perceived_param_lt_3009 : new_perceived_param < (0.3009 : ℝ) := by
  have h_exact : (0.578 : ℝ) / (2.7182818283 : ℝ) * (1.4142135624 : ℝ) < (0.3009 : ℝ) := by norm_num
  unfold new_perceived_param gamma_euler e sqrt2
  have hγ_pos : (0 : ℝ) < gamma_euler / (2.7182818283 : ℝ) := div_pos gamma_euler_pos (by norm_num)
  have hsqrt_pos : (0 : ℝ) < sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have hdiv_core : gamma_euler / exp 1 < gamma_euler / (2.7182818283 : ℝ) :=
    div_lt_div_of_pos_left gamma_euler_pos (by norm_num) exp_one_gt_d9
  have hdiv := mul_lt_mul_of_pos_right hdiv_core hsqrt_pos
  have hsqrt := mul_lt_mul_of_pos_left sqrt_two_lt_14142135624 hγ_pos
  have hγ := mul_lt_mul_of_pos_right
    (div_lt_div_of_pos_right
      (by norm_num : (0.57721566490153286060651209008240243 : ℝ) < (0.578 : ℝ))
      (by norm_num : (0 : ℝ) < (2.7182818283 : ℝ)))
    (by norm_num : (0 : ℝ) < (1.4142135624 : ℝ))
  exact lt_trans hdiv (lt_trans hsqrt (lt_trans hγ h_exact))

lemma new_perceived_param_gt_030 : (0.300 : ℝ) < new_perceived_param := by
  have h_exact : (0.300 : ℝ) <
      (0.57721566490153286060651209008240243 : ℝ) / (2.7182818286 : ℝ) * (1.4142135623 : ℝ) := by
    norm_num
  unfold new_perceived_param gamma_euler e sqrt2
  have hdiv : gamma_euler / (2.7182818286 : ℝ) < gamma_euler / exp 1 :=
    div_lt_div_of_pos_left gamma_euler_pos (exp_pos _) (by linarith [exp_one_lt_d9])
  have hsqrt : (1.4142135623 : ℝ) < sqrt 2 := Real.lt_sqrt_of_sq_lt (by norm_num)
  have hmid := mul_lt_mul_of_pos_right hdiv (by norm_num : (0 : ℝ) < 1.4142135623)
  have hγexp_pos : (0 : ℝ) < gamma_euler / exp 1 := div_pos gamma_euler_pos (exp_pos 1)
  have hprod := mul_lt_mul_of_pos_left hsqrt hγexp_pos
  exact lt_trans h_exact (lt_trans hmid hprod)

lemma new_perceived_param_gt_30030 : (0.30030 : ℝ) < new_perceived_param := by
  have h_exact : (0.30030 : ℝ) <
      (0.57721566490153286060651209008240243 : ℝ) / (2.7182818286 : ℝ) * (1.4142135623 : ℝ) := by
    norm_num
  unfold new_perceived_param gamma_euler e sqrt2
  have hdiv : gamma_euler / (2.7182818286 : ℝ) < gamma_euler / exp 1 :=
    div_lt_div_of_pos_left gamma_euler_pos (exp_pos _) (by linarith [exp_one_lt_d9])
  have hsqrt : (1.4142135623 : ℝ) < sqrt 2 := Real.lt_sqrt_of_sq_lt (by norm_num)
  have hmid := mul_lt_mul_of_pos_right hdiv (by norm_num : (0 : ℝ) < 1.4142135623)
  have hγexp_pos : (0 : ℝ) < gamma_euler / exp 1 := div_pos gamma_euler_pos (exp_pos 1)
  have hprod := mul_lt_mul_of_pos_left hsqrt hγexp_pos
  exact lt_trans h_exact (lt_trans hmid hprod)

lemma new_perceived_param_lt_30032 : new_perceived_param < (0.30032 : ℝ) := by
  have h_exact :
      (0.57721566490153286060651209008240243 : ℝ) / (2.7182818283 : ℝ) * (1.4142135624 : ℝ) <
        (0.30032 : ℝ) := by
    norm_num
  unfold new_perceived_param gamma_euler e sqrt2
  have hγ_pos : (0 : ℝ) < gamma_euler / (2.7182818283 : ℝ) := div_pos gamma_euler_pos (by norm_num)
  have hsqrt_pos : (0 : ℝ) < sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have hdiv_core : gamma_euler / exp 1 < gamma_euler / (2.7182818283 : ℝ) :=
    div_lt_div_of_pos_left gamma_euler_pos (by norm_num) exp_one_gt_d9
  have hdiv := mul_lt_mul_of_pos_right hdiv_core hsqrt_pos
  have hsqrt := mul_lt_mul_of_pos_left sqrt_two_lt_14142135624 hγ_pos
  exact lt_trans hdiv (lt_trans hsqrt h_exact)

lemma log_ratio_lo
    (p : FSOTParams)
    (h_D : (20 : ℝ) ≤ p.D_eff) :
    log (0.8 : ℝ) ≤ log (p.D_eff / 25) := by
  have h_frac : (0.8 : ℝ) ≤ p.D_eff / 25 := by
    have : (20 : ℝ) ≤ p.D_eff := h_D
    linarith
  have h_pos : (0 : ℝ) < p.D_eff / 25 := div_pos (by linarith [h_D]) (by norm_num)
  exact log_le_log (by norm_num : (0 : ℝ) < 0.8) h_frac

lemma log_ratio_hi
    (p : FSOTParams)
    (h_lo : (20 : ℝ) ≤ p.D_eff)
    (h_hi : p.D_eff ≤ (30 : ℝ)) :
    log (p.D_eff / 25) ≤ log (1.2 : ℝ) := by
  have h_frac : p.D_eff / 25 ≤ (1.2 : ℝ) := by linarith [h_hi]
  have h_pos : (0 : ℝ) < p.D_eff / 25 := div_pos (by linarith [h_lo]) (by norm_num)
  exact log_le_log h_pos h_frac

lemma new_perceived_param_pos : (0 : ℝ) < new_perceived_param :=
  lt_trans (by norm_num) new_perceived_param_gt_030

lemma perceived_adjust_lo
    (p : FSOTParams)
    (h_D : (20 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 30) :
    (0.91 : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25) := by
  have h_mul_le : new_perceived_param * log (0.8 : ℝ) ≤ new_perceived_param * log (p.D_eff / 25) := by
    apply mul_le_mul_of_nonneg_left (log_ratio_lo p h_D.1) (le_of_lt new_perceived_param_pos)
  have h_floor : new_perceived_param * log (0.8 : ℝ) > -(0.09 : ℝ) := by
    have h_mul := mul_lt_mul_of_pos_right log_08_gt_m0298 new_perceived_param_pos
    nlinarith [new_perceived_param_lt_031, h_mul]
  linarith [h_mul_le, h_floor]

lemma perceived_adjust_hi
    (p : FSOTParams)
    (h_D : (20 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 30) :
    1 + new_perceived_param * log (p.D_eff / 25) < (1.1 : ℝ) := by
  have h_mul_le : new_perceived_param * log (p.D_eff / 25) ≤ new_perceived_param * log (1.2 : ℝ) := by
    apply mul_le_mul_of_nonneg_left (log_ratio_hi p h_D.1 h_D.2) (le_of_lt new_perceived_param_pos)
  have h_ceil : new_perceived_param * log (1.2 : ℝ) < (0.1 : ℝ) := by
    have h1 := mul_lt_mul_of_pos_left log_12_lt new_perceived_param_pos
    nlinarith [h1, new_perceived_param_lt_031]
  linarith [h_mul_le, h_ceil]

def cosmologicalParams : FSOTParams :=
  { D_eff := 25, observed := false, delta_psi := 1.0 }

lemma cosmological_perceived_adjust_eq_one :
    1 + new_perceived_param * log (cosmologicalParams.D_eff / 25) = 1 := by
  simp [cosmologicalParams, log_one]

lemma psi_con_pos : (0 : ℝ) < psi_con := lt_trans (by norm_num) psi_con_gt_632

lemma psi_con_eta_pos : (0 : ℝ) < psi_con * eta_eff :=
  mul_pos psi_con_pos eta_pos

lemma psi_con_eta_lt_pi : psi_con * eta_eff < pi := by
  have h_prod : psi_con * eta_eff < (0.633 : ℝ) * (0.467 : ℝ) :=
    mul_lt_mul_of_pos psi_con_lt_633 eta_eff_lt_467 (by linarith [psi_con_pos]) (by linarith [eta_pos])
  unfold pi
  nlinarith [h_prod, pi_gt_d4]

lemma psi_con_eta_prod_lt_three_tenths : psi_con * eta_eff < (0.3 : ℝ) := by
  have h_prod : psi_con * eta_eff < (0.633 : ℝ) * (0.467 : ℝ) :=
    mul_lt_mul_of_pos psi_con_lt_633 eta_eff_lt_467 (by linarith [psi_con_pos]) (by linarith [eta_pos])
  nlinarith [h_prod]

lemma theta_s_pos : (0 : ℝ) < theta_s := by
  unfold theta_s
  exact sin_pos_of_pos_of_lt_pi psi_con_eta_pos psi_con_eta_lt_pi

lemma theta_s_le_one : theta_s ≤ (1 : ℝ) := by
  unfold theta_s
  exact sin_le_one _

lemma theta_s_le_pi : theta_s ≤ pi := by linarith [theta_s_le_one, pi_gt_one]

lemma sin_theta_s_nonneg : (0 : ℝ) ≤ sin theta_s :=
  sin_nonneg_of_mem_Icc ⟨le_of_lt theta_s_pos, theta_s_le_pi⟩

lemma sin_div_phi_le_one : sin theta_s / phi ≤ 1 := by
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  rw [div_le_iff₀ hφ]
  linarith [sin_le_one theta_s, phi_gt_one]

lemma poof_factor_lt_one : poof_factor < 1 := by
  unfold poof_factor
  apply exp_lt_one_iff.mpr
  have h_denom : 0 < eta_eff * log phi := mul_pos eta_pos (log_pos phi_gt_one)
  have h_num : -(log pi / e) < 0 := neg_neg_of_pos (div_pos (log_pos pi_gt_one) (exp_pos 1))
  exact div_neg_of_neg_of_pos h_num h_denom

lemma exp_0572_lt_1772 : exp (0.572 : ℝ) < (1.772 : ℝ) := by
  have h :=
    Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.572) (by norm_num : (0.572 : ℝ) ≤ 1) (n := 5)
      (by norm_num)
  nlinarith [h]

lemma exp_1144_lt_31415 : exp (1.144 : ℝ) < (3.1415 : ℝ) := by
  rw [show (1.144 : ℝ) = 0.572 + 0.572 by norm_num, Real.exp_add]
  have h_mul :=
    mul_lt_mul_of_pos exp_0572_lt_1772 exp_0572_lt_1772 (exp_pos _) (by norm_num : (0 : ℝ) < 1.772)
  have h_bound : (1.772 : ℝ) * (1.772 : ℝ) < (3.1415 : ℝ) := by norm_num
  exact lt_trans h_mul h_bound

lemma log_31415_gt_1144 : (1.144 : ℝ) < log (3.1415 : ℝ) :=
  (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 3.1415)).2 exp_1144_lt_31415

lemma log_pi_gt_1144 : (1.144 : ℝ) < log pi := by
  have hpi : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
  exact lt_trans log_31415_gt_1144 (log_lt_log (by norm_num) hpi)

lemma exp_11445_lt_3141592 : exp (1.1445 : ℝ) < (3.141592 : ℝ) := by
  rw [show (1.1445 : ℝ) = 0.57225 + 0.57225 by norm_num, Real.exp_add]
  have h_upper :=
    Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.57225) (by norm_num : (0.57225 : ℝ) ≤ 1) (n := 6)
      (by norm_num)
  have h_mul : exp 0.57225 * exp 0.57225 < (1.77245 : ℝ) * (1.77245 : ℝ) := by
    nlinarith [h_upper, exp_pos 0.57225]
  have h_bound : (1.77245 : ℝ) * (1.77245 : ℝ) < (3.141592 : ℝ) := by norm_num
  exact lt_trans h_mul h_bound

lemma log_pi_gt_11445 : (1.1445 : ℝ) < log pi := by
  have hpi : (3.141592 : ℝ) < pi := by unfold pi; exact pi_gt_d6
  have h := (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 3.141592)).2 exp_11445_lt_3141592
  exact lt_trans h (log_lt_log (by norm_num) hpi)

lemma log_pi_div_e_gt_421 : (0.421 : ℝ) < log pi / e := by
  have h_lo : (0.421 : ℝ) * e < log pi := by
    unfold e
    have h_mul := (by norm_num : (0.421 : ℝ) * (2.7182818286 : ℝ) < (1.1445 : ℝ))
    nlinarith [log_pi_gt_11445, h_mul, exp_one_lt_d9]
  unfold e
  rw [lt_div_iff₀ (exp_pos 1)]
  exact h_lo

lemma exp_0245_gt_1275 : (1.275 : ℝ) < exp 0.245 := by
  have h_poly : (1.275 : ℝ) < 1 + (0.245 : ℝ) + (0.245 : ℝ) ^ 2 / 2 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 0.245) 3
  have h_eq :
      (1 + (0.245 : ℝ) + (0.245 : ℝ) ^ 2 / 2 : ℝ) =
        ∑ i ∈ Finset.range 3, (0.245 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma exp_049_gt_16181 : (1.6181 : ℝ) < exp 0.49 := by
  rw [show (0.49 : ℝ) = 0.245 + 0.245 by norm_num, Real.exp_add]
  have h_mul :=
    mul_lt_mul_of_pos exp_0245_gt_1275 exp_0245_gt_1275 (by norm_num : (0 : ℝ) < 1.275) (exp_pos 0.245)
  have h_floor : (1.6181 : ℝ) < (1.275 : ℝ) * (1.275 : ℝ) := by norm_num
  exact lt_trans h_floor h_mul

lemma exp_04813_gt_16181 : (1.6181 : ℝ) < exp 0.4813 := by
  set t : ℝ := 0.4813 with ht
  have h_poly :
      (1.6181 : ℝ) < 1 + t + t ^ 2 / 2 + t ^ 3 / 6 + t ^ 4 / 24 + t ^ 5 / 120 + t ^ 6 / 720 := by
    rw [ht]
    norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 0.4813) 7
  have h_eq :
      (1 + t + t ^ 2 / 2 + t ^ 3 / 6 + t ^ 4 / 24 + t ^ 5 / 120 + t ^ 6 / 720 : ℝ) =
        ∑ i ∈ Finset.range 7, t ^ i / Nat.factorial i := by
    rw [ht]
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma log_16181_lt_04813 : log (1.6181 : ℝ) < (0.4813 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 1.6181)).2 exp_04813_gt_16181

lemma log_phi_lt_04813 : log phi < (0.4813 : ℝ) := by
  have h_log_hi : log phi < log (1.6181 : ℝ) :=
    log_lt_log (by linarith [phi_gt_1618]) phi_lt_16181
  exact lt_trans h_log_hi log_16181_lt_04813

lemma log_phi_lt_0482 : log phi < (0.482 : ℝ) :=
  lt_trans log_phi_lt_04813 (by norm_num : (0.4813 : ℝ) < (0.482 : ℝ))

lemma eta_log_phi_lt_0225 : eta_eff * log phi < (0.225 : ℝ) := by
  have h_prod :=
    mul_lt_mul_of_pos eta_eff_lt_467 log_phi_lt_04813 eta_pos (by norm_num : (0 : ℝ) < 0.4813)
  have h_bound : (0.467 : ℝ) * (0.4813 : ℝ) < (0.225 : ℝ) := by norm_num
  exact lt_trans h_prod h_bound

lemma exp_185_gt_626 : (6.26 : ℝ) < exp 1.85 := by
  have h_poly :
      (6.26 : ℝ) < 1 + (1.85 : ℝ) + (1.85 : ℝ) ^ 2 / 2 + (1.85 : ℝ) ^ 3 / 6 + (1.85 : ℝ) ^ 4 / 24 +
        (1.85 : ℝ) ^ 5 / 120 + (1.85 : ℝ) ^ 6 / 720 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 1.85) 7
  have h_eq :
      (1 + (1.85 : ℝ) + (1.85 : ℝ) ^ 2 / 2 + (1.85 : ℝ) ^ 3 / 6 + (1.85 : ℝ) ^ 4 / 24 +
          (1.85 : ℝ) ^ 5 / 120 + (1.85 : ℝ) ^ 6 / 720 : ℝ) =
        ∑ i ∈ Finset.range 7, (1.85 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma exp_neg_185_lt_016 : exp (-1.85) < (0.16 : ℝ) := by
  have h_eq : exp (-1.85) = 1 / exp 1.85 := by
    rw [show (-1.85 : ℝ) = -(1.85) by norm_num, exp_neg, inv_eq_one_div]
  rw [h_eq]
  have h_inv := one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < 6.26) exp_185_gt_626
  have h_small : (1 / (6.26 : ℝ)) < (0.16 : ℝ) := by norm_num
  exact lt_trans h_inv h_small

lemma log_016_gt_m185 : (-1.85 : ℝ) < log (0.16 : ℝ) :=
  (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 0.16)).2 exp_neg_185_lt_016

lemma poof_factor_lt_point_one_six : poof_factor < (0.16 : ℝ) := by
  unfold poof_factor
  have h_denom_pos : (0 : ℝ) < eta_eff * log phi := mul_pos eta_pos (log_pos phi_gt_one)
  have h_ratio : (1.85 : ℝ) < (log pi / e) / (eta_eff * log phi) := by
    rw [lt_div_iff₀ h_denom_pos]
    nlinarith [log_pi_div_e_gt_421, eta_log_phi_lt_0225]
  have h_strict : -(log pi / e) / (eta_eff * log phi) < (-1.85 : ℝ) := by
    have := neg_lt_neg h_ratio
    simpa [div_eq_mul_inv, mul_assoc] using this
  have h_neg : -(log pi / e) / (eta_eff * log phi) < log (0.16 : ℝ) :=
    lt_trans h_strict log_016_gt_m185
  have h := (exp_lt_exp).2 h_neg
  rwa [exp_log (by norm_num : (0 : ℝ) < 0.16)] at h

lemma alpha_nonneg : (0 : ℝ) ≤ alpha := by
  unfold alpha
  apply div_nonneg (log_nonneg (le_of_lt pi_gt_one))
  exact mul_nonneg (le_of_lt (exp_pos 1)) (pow_nonneg (le_of_lt (lt_trans (by norm_num) phi_gt_one)) _)

lemma coherence_efficiency_lt_ten : coherence_efficiency < (10 : ℝ) := by
  unfold coherence_efficiency
  have h_poof_pos : 0 < poof_factor := exp_pos _
  have h1 : 1 - poof_factor * sin theta_s ≤ (3 : ℝ) := by
    nlinarith [poof_factor_lt_one, h_poof_pos, sin_le_one theta_s, sin_theta_s_nonneg]
  have h2 : 1 + 0.01 * catalan_G / (pi * phi) ≤ (3 : ℝ) := by
    have h_small : 0.01 * catalan_G / (pi * phi) ≤ (1 : ℝ) := by
      unfold catalan_G
      have h_den : (0 : ℝ) < pi * phi := by nlinarith [phi_gt_one, pi_gt_one]
      rw [div_le_iff₀ h_den]
      nlinarith [phi_gt_one, pi_gt_one]
    linarith [h_small]
  have h1pos : 0 < 1 - poof_factor * sin theta_s := by
    have h_le : poof_factor * sin theta_s ≤ poof_factor := by
      simpa using mul_le_mul_of_nonneg_left (sin_le_one theta_s) (le_of_lt h_poof_pos)
    exact sub_pos.mpr (lt_of_le_of_lt h_le poof_factor_lt_one)
  have h2pos : 0 < 1 + 0.01 * catalan_G / (pi * phi) := by
    have hphi_pos : 0 < phi := lt_trans (by norm_num) phi_gt_one
    exact add_pos (by norm_num) (div_pos (mul_pos (by norm_num) (by unfold catalan_G; norm_num)) (mul_pos Real.pi_pos hphi_pos))
  calc (1 - poof_factor * sin theta_s) * (1 + 0.01 * catalan_G / (pi * phi))
      ≤ (3 : ℝ) * 3 := mul_le_mul h1 h2 (le_of_lt h2pos) (by norm_num)
    _ < 10 := by norm_num

lemma cosmological_cos_arg_lo :
    (3.4 : ℝ) < (psi_con + cosmologicalParams.delta_psi) / eta_eff := by
  simp only [cosmologicalParams]
  have h_num : (1.632 : ℝ) < psi_con + 1 := by linarith [psi_con_gt_632]
  have h_div : (1.632 : ℝ) / eta_eff < (psi_con + 1) / eta_eff :=
    div_lt_div_of_pos_right h_num eta_pos
  have h_eta : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
  have h_lo : (1.632 : ℝ) / (0.467 : ℝ) < (1.632 : ℝ) / eta_eff := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
    exact h_eta
  have h_num_bound : (3.4 : ℝ) < (1.632 : ℝ) / (0.467 : ℝ) := by norm_num
  linarith [h_div, h_lo, h_num_bound]

lemma cosmological_cos_arg_hi :
    (psi_con + cosmologicalParams.delta_psi) / eta_eff < (3.6 : ℝ) := by
  simp only [cosmologicalParams]
  have h_num : psi_con + 1 < (1.633 : ℝ) := by linarith [psi_con_lt_633]
  have h_div : (psi_con + 1) / eta_eff < (1.633 : ℝ) / eta_eff :=
    div_lt_div_of_pos_right h_num eta_pos
  have h_eta : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_hi : (1.633 : ℝ) / eta_eff < (1.633 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta
  have h_num_bound : (1.633 : ℝ) / (0.466 : ℝ) < (3.6 : ℝ) := by norm_num
  linarith [h_div, h_hi, h_num_bound]

lemma cosmological_cos_lt_neg_half :
    cos ((psi_con + cosmologicalParams.delta_psi) / eta_eff) < -(0.5 : ℝ) := by
  set arg := (psi_con + cosmologicalParams.delta_psi) / eta_eff
  have h_lo := cosmological_cos_arg_lo
  have h_hi := cosmological_cos_arg_hi
  have hpi_hi : pi < (3.1416 : ℝ) := by unfold pi; exact pi_lt_d4
  have hpi_lo : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
  have h_pi_lo : pi < arg := by
    simp only [arg, cosmologicalParams] at h_lo ⊢
    linarith [h_lo, hpi_hi]
  have h_arg_lo : (3.4 : ℝ) < arg := by simpa [arg, cosmologicalParams] using h_lo
  have h_arg_hi : arg < (3.6 : ℝ) := by simpa [arg, cosmologicalParams] using h_hi
  have h_t_lo : (0.258 : ℝ) < arg - pi := by linarith [h_arg_lo, hpi_hi]
  have h_t_hi : arg - pi < (0.459 : ℝ) := by linarith [h_arg_hi, hpi_lo]
  have h_upper : arg - pi ≤ pi := by linarith [h_t_hi, hpi_lo]
  have h_t_in : arg - pi ∈ Set.Icc (0 : ℝ) π := by
    refine ⟨by linarith [h_t_lo], ?_⟩
    simpa [pi_eq_real_pi] using h_upper
  have h_cos_eq : cos arg = -cos (arg - pi) := by
    calc cos arg = cos ((arg - pi) + pi) := by ring_nf
      _ = -cos (arg - pi) := cos_add_pi (arg - pi)
  have h_antitone := Real.antitoneOn_cos
  have h046_in : (0.46 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h05_in : (0.5 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_pi4_in : pi / 4 ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_05_lt_pi4 : (0.5 : ℝ) < pi / 4 := by unfold pi; nlinarith [pi_gt_d4]
  have h_cos_pi4 : cos (pi / 4) = Real.sqrt 2 / 2 := by
    simp [pi_eq_real_pi, Real.cos_pi_div_four]
  have h_sqrt2 : (1.414 : ℝ) < Real.sqrt 2 := Real.lt_sqrt_of_sq_lt (by norm_num)
  have h_sqrt_lo : (0.7 : ℝ) < Real.sqrt 2 / 2 := by nlinarith [h_sqrt2]
  have h_cos_05_gt_half : (1 / 2 : ℝ) < cos (0.5) := by
    have h := h_antitone h05_in h_pi4_in (le_of_lt h_05_lt_pi4)
    linarith [h, h_cos_pi4, h_sqrt_lo]
  have h_cos_046_ge_05 : cos (0.5) ≤ cos (0.46) :=
    h_antitone h046_in h05_in (by norm_num : (0.46 : ℝ) ≤ 0.5)
  have h_le_046 : arg - pi ≤ (0.46 : ℝ) := by linarith [h_t_hi]
  have h_cos_t_ge_046 : cos (0.46) ≤ cos (arg - pi) :=
    h_antitone h_t_in h046_in h_le_046
  linarith [h_cos_eq, h_cos_t_ge_046, h_cos_046_ge_05, h_cos_05_gt_half]

lemma bleed_in_factor_nonneg : (0 : ℝ) ≤ bleed_in_factor := by
  unfold bleed_in_factor
  have h_coherence : (0 : ℝ) < coherence_efficiency := by
    unfold coherence_efficiency
    have h_poof_pos : 0 < poof_factor := exp_pos _
    have h_prod_lt_one : poof_factor * sin theta_s < 1 := by
      have h_le : poof_factor * sin theta_s ≤ poof_factor := by
        simpa using mul_le_mul_of_nonneg_left (sin_le_one theta_s) (le_of_lt h_poof_pos)
      exact lt_of_le_of_lt h_le poof_factor_lt_one
    exact mul_pos (sub_pos.mpr h_prod_lt_one) (by
      have hphi_pos : 0 < phi := lt_trans (by norm_num) phi_gt_one
      exact add_pos (by norm_num) (div_pos (mul_pos (by norm_num) (by unfold catalan_G; norm_num)) (mul_pos Real.pi_pos hphi_pos)))
  apply mul_nonneg (le_of_lt h_coherence)
  linarith [sin_div_phi_le_one, sin_theta_s_nonneg]

lemma bleed_in_factor_pos : (0 : ℝ) < bleed_in_factor := by
  unfold bleed_in_factor
  have h_coh : (0 : ℝ) < coherence_efficiency := by
    unfold coherence_efficiency
    have h_poof_pos : 0 < poof_factor := exp_pos _
    have h_prod_lt_one : poof_factor * sin theta_s < 1 := by
      have h_le : poof_factor * sin theta_s ≤ poof_factor := by
        simpa using mul_le_mul_of_nonneg_left (sin_le_one theta_s) (le_of_lt h_poof_pos)
      exact lt_of_le_of_lt h_le poof_factor_lt_one
    exact mul_pos (sub_pos.mpr h_prod_lt_one) (by
      have hphi_pos : 0 < phi := lt_trans (by norm_num) phi_gt_one
      exact add_pos (by norm_num) (div_pos (mul_pos (by norm_num) (by unfold catalan_G; norm_num)) (mul_pos Real.pi_pos hphi_pos)))
  have h_inner : (0 : ℝ) < 1 - sin theta_s / phi := by
    have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
    have h_div_lt_one : sin theta_s / phi < 1 := by
      rw [div_lt_iff₀ hφ]
      linarith [sin_le_one theta_s, phi_gt_one]
    exact sub_pos.mpr h_div_lt_one
  exact mul_pos h_coh h_inner

lemma cosmological_exp_factor_gt_two :
    (2 : ℝ) < exp (1 + bleed_in_factor * cosmologicalParams.delta_psi) := by
  have h_exp1 : Real.exp 1 < exp (1 + bleed_in_factor * cosmologicalParams.delta_psi) := by
    simp only [cosmologicalParams]
    exact Real.exp_lt_exp.mpr (by linarith [bleed_in_factor_pos])
  have h_e : (2 : ℝ) < Real.exp 1 := by
    linarith [Real.add_one_lt_exp (by norm_num : (1 : ℝ) ≠ 0)]
  exact lt_trans h_e h_exp1

lemma theta_s_lt_three_tenths : theta_s < (0.3 : ℝ) := by
  unfold theta_s
  exact lt_trans (Real.sin_lt psi_con_eta_pos) psi_con_eta_prod_lt_three_tenths

lemma coherence_correction_gt_one : (1 : ℝ) < 1 + 0.01 * catalan_G / (pi * phi) := by
  have hphi_pos : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have h_den_pos : (0 : ℝ) < pi * phi := mul_pos Real.pi_pos hphi_pos
  have h_num_pos : (0 : ℝ) < 0.01 * catalan_G := by unfold catalan_G; norm_num
  have h_div_pos : (0 : ℝ) < 0.01 * catalan_G / (pi * phi) := div_pos h_num_pos h_den_pos
  linarith

lemma coherence_efficiency_gt_nine_five : (0.95 : ℝ) < coherence_efficiency := by
  unfold coherence_efficiency
  have h_poof_pos : 0 < poof_factor := exp_pos _
  have h_psin_lt : poof_factor * sin theta_s < (0.05 : ℝ) := by
    have h_sin_le : sin theta_s ≤ theta_s := Real.sin_le (le_of_lt theta_s_pos)
    nlinarith [poof_factor_lt_point_one_six, h_sin_le, theta_s_lt_three_tenths, h_poof_pos]
  have h_first : (0.95 : ℝ) < 1 - poof_factor * sin theta_s := by linarith [h_psin_lt]
  have h_second := coherence_correction_gt_one
  have h_second_pos : (0 : ℝ) < 1 + 0.01 * catalan_G / (pi * phi) := by linarith [h_second]
  simpa [mul_one] using
    mul_lt_mul_of_pos h_first h_second (by norm_num : (0 : ℝ) < (0.95 : ℝ)) h_second_pos

lemma coherence_efficiency_gt_seven_tenths : (0.7 : ℝ) < coherence_efficiency :=
  lt_trans (by norm_num : (0.7 : ℝ) < (0.95 : ℝ)) coherence_efficiency_gt_nine_five

lemma bleed_in_inner_gt_eight_one_four : (0.814 : ℝ) < 1 - sin theta_s / phi := by
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have h_sin_small : sin theta_s / phi < (0.186 : ℝ) := by
    rw [div_lt_iff₀ hφ]
    have h_sin_le : sin theta_s ≤ theta_s := Real.sin_le (le_of_lt theta_s_pos)
    have h_sin_lt : sin theta_s < (0.3 : ℝ) := lt_of_le_of_lt h_sin_le theta_s_lt_three_tenths
    nlinarith [h_sin_lt, phi_gt_1618, (by norm_num : (0.3 : ℝ) / (1.618 : ℝ) < (0.186 : ℝ))]
  linarith

lemma bleed_in_inner_pos : (0 : ℝ) < 1 - sin theta_s / phi := by
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have h_div_lt_one : sin theta_s / phi < 1 := by
    rw [div_lt_iff₀ hφ]
    linarith [sin_le_one theta_s, phi_gt_one]
  exact sub_pos.mpr h_div_lt_one

lemma bleed_in_factor_gt_six_tenths : (0.6 : ℝ) < bleed_in_factor := by
  unfold bleed_in_factor
  have h_prod :
      (0.95 : ℝ) * (0.814 : ℝ) <
        coherence_efficiency * (1 - sin theta_s / phi) :=
    mul_lt_mul_of_pos coherence_efficiency_gt_nine_five bleed_in_inner_gt_eight_one_four
      (by linarith [coherence_efficiency_gt_nine_five]) bleed_in_inner_pos
  have h_floor : (0.6 : ℝ) < (0.95 : ℝ) * (0.814 : ℝ) := by norm_num
  exact lt_trans h_floor h_prod

lemma bleed_in_factor_gt_seven_seven : (0.77 : ℝ) < bleed_in_factor := by
  unfold bleed_in_factor
  have h_prod :
      (0.95 : ℝ) * (0.814 : ℝ) <
        coherence_efficiency * (1 - sin theta_s / phi) :=
    mul_lt_mul_of_pos coherence_efficiency_gt_nine_five bleed_in_inner_gt_eight_one_four
      (by linarith [coherence_efficiency_gt_nine_five]) bleed_in_inner_pos
  have h_floor : (0.77 : ℝ) < (0.95 : ℝ) * (0.814 : ℝ) := by norm_num
  exact lt_trans h_floor h_prod

lemma exp_077_gt_184 : (1.84 : ℝ) < exp 0.77 := by
  rw [show (0.77 : ℝ) = 0.5 + 0.27 by norm_num, Real.exp_add]
  have h1 : (1.5 : ℝ) < exp 0.5 := by nlinarith [Real.add_one_lt_exp (by norm_num : (0.5 : ℝ) ≠ 0)]
  have h2 : (1.27 : ℝ) < exp 0.27 := by nlinarith [Real.add_one_lt_exp (by norm_num : (0.27 : ℝ) ≠ 0)]
  nlinarith [h1, h2]

lemma exp_177_gt_five : (5 : ℝ) < exp 1.77 := by
  rw [show (1.77 : ℝ) = 1 + 0.77 by norm_num, Real.exp_add]
  nlinarith [exp_one_gt_d9, exp_077_gt_184]

lemma log_five_lt_one_seven_seven : log 5 < (1.77 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 5)).2 exp_177_gt_five

lemma cosmological_exp_factor_gt_five :
    (5 : ℝ) < exp (1 + bleed_in_factor * cosmologicalParams.delta_psi) := by
  simp only [cosmologicalParams]
  have h_bleed : (1.77 : ℝ) < 1 + bleed_in_factor * (1.0 : ℝ) := by
    linarith [bleed_in_factor_gt_seven_seven]
  have h_log : log 5 < 1 + bleed_in_factor * (1.0 : ℝ) := lt_trans log_five_lt_one_seven_seven h_bleed
  exact (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 5)).1 h_log

lemma cosmological_cos_arg_hi_tight :
    (psi_con + cosmologicalParams.delta_psi) / eta_eff < (3.51 : ℝ) := by
  simp only [cosmologicalParams]
  have h_num : psi_con + 1 < (1.633 : ℝ) := by linarith [psi_con_lt_633]
  have h_div : (psi_con + 1) / eta_eff < (1.633 : ℝ) / eta_eff :=
    div_lt_div_of_pos_right h_num eta_pos
  have h_eta : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_hi : (1.633 : ℝ) / eta_eff < (1.633 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta
  have h_num_bound : (1.633 : ℝ) / (0.466 : ℝ) < (3.51 : ℝ) := by norm_num
  linarith [h_div, h_hi, h_num_bound]

lemma cosmological_cos_t_hi :
    (psi_con + cosmologicalParams.delta_psi) / eta_eff - pi < (0.37 : ℝ) := by
  have h_arg_hi := cosmological_cos_arg_hi_tight
  have hpi_lo : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
  simp only [cosmologicalParams] at h_arg_hi ⊢
  linarith [h_arg_hi, hpi_lo]

lemma cosmological_cos_lt_neg_093 :
    cos ((psi_con + cosmologicalParams.delta_psi) / eta_eff) < -(0.93 : ℝ) := by
  set arg := (psi_con + cosmologicalParams.delta_psi) / eta_eff
  have h_t_hi := cosmological_cos_t_hi
  have hpi_hi : pi < (3.1416 : ℝ) := by unfold pi; exact pi_lt_d4
  have h_t_lo : (0 : ℝ) < arg - pi := by
    have h_arg_lo := cosmological_cos_arg_lo
    simp only [arg, cosmologicalParams] at h_arg_lo ⊢
    linarith [h_arg_lo, hpi_hi]
  have h_t_in : arg - pi ∈ Set.Icc (0 : ℝ) π := by
    refine ⟨le_of_lt h_t_lo, ?_⟩
    have h_upper : arg - pi ≤ pi := by
      have h_hi' : arg - pi < (0.37 : ℝ) := by simpa [arg, cosmologicalParams] using h_t_hi
      linarith [h_hi', pi_gt_one]
    simpa [pi_eq_real_pi] using h_upper
  have h_cos_eq : cos arg = -cos (arg - pi) := by
    calc cos arg = cos ((arg - pi) + pi) := by ring_nf
      _ = -cos (arg - pi) := cos_add_pi (arg - pi)
  have h037_in : (0.37 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos_037_gt_093 : (0.93 : ℝ) < cos (0.37) := by
    have h := Real.one_sub_sq_div_two_lt_cos (by norm_num : (0.37 : ℝ) ≠ 0)
    have h_sq : (0.37 : ℝ) ^ 2 / 2 < (0.07 : ℝ) := by norm_num
    linarith [h, h_sq]
  have h_antitone := Real.antitoneOn_cos
  have h_cos_t_gt_037 : cos (0.37) ≤ cos (arg - pi) :=
    h_antitone h_t_in h037_in (le_of_lt (by simpa [arg, cosmologicalParams] using h_t_hi))
  linarith [h_cos_eq, h_cos_t_gt_037, h_cos_037_gt_093]

lemma dark_energy_cos_arg_hi :
    (psi_con + (1.1 : ℝ)) / eta_eff < (3.72 : ℝ) := by
  have h_num : psi_con + (1.1 : ℝ) < (1.733 : ℝ) := by linarith [psi_con_lt_633]
  have h_div : (psi_con + (1.1 : ℝ)) / eta_eff < (1.733 : ℝ) / eta_eff :=
    div_lt_div_of_pos_right h_num eta_pos
  have h_eta : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_hi : (1.733 : ℝ) / eta_eff < (1.733 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta
  have h_num_bound : (1.733 : ℝ) / (0.466 : ℝ) < (3.72 : ℝ) := by norm_num
  linarith [h_div, h_hi, h_num_bound]

lemma dark_energy_cos_t_hi : (psi_con + (1.1 : ℝ)) / eta_eff - pi < (0.58 : ℝ) := by
  have h_arg_hi := dark_energy_cos_arg_hi
  have hpi_lo : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
  linarith [h_arg_hi, hpi_lo]

lemma dark_energy_cos_lt_neg_083 :
    cos ((psi_con + (1.1 : ℝ)) / eta_eff) < -(0.83 : ℝ) := by
  set arg := (psi_con + (1.1 : ℝ)) / eta_eff
  have h_t_hi := dark_energy_cos_t_hi
  have hpi_hi : pi < (3.1416 : ℝ) := by unfold pi; exact pi_lt_d4
  have h_arg_lo : (3.4 : ℝ) < arg := by
    have h_num : (1.632 : ℝ) < psi_con + (1.1 : ℝ) := by linarith [psi_con_gt_632]
    have h_div : (1.632 : ℝ) / eta_eff < (psi_con + (1.1 : ℝ)) / eta_eff :=
      div_lt_div_of_pos_right h_num eta_pos
    have h_eta : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
    have h_lo : (1.632 : ℝ) / (0.467 : ℝ) < (1.632 : ℝ) / eta_eff := by
      rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
      exact h_eta
    have h_num_bound : (3.4 : ℝ) < (1.632 : ℝ) / (0.467 : ℝ) := by norm_num
    simpa [arg] using lt_trans h_num_bound (lt_trans h_lo h_div)
  have h_t_lo : (0 : ℝ) < arg - pi := by linarith [h_arg_lo, hpi_hi]
  have h_t_in : arg - pi ∈ Set.Icc (0 : ℝ) π := by
    refine ⟨le_of_lt h_t_lo, ?_⟩
    have h_upper : arg - pi ≤ pi := by
      have h_hi' : arg - pi < (0.58 : ℝ) := by simpa [arg] using h_t_hi
      linarith [h_hi', pi_gt_one]
    simpa [pi_eq_real_pi] using h_upper
  have h_cos_eq : cos arg = -cos (arg - pi) := by
    calc cos arg = cos ((arg - pi) + pi) := by ring_nf
      _ = -cos (arg - pi) := cos_add_pi (arg - pi)
  have h058_in : (0.58 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos_058_gt_083 : (0.83 : ℝ) < cos (0.58) := by
    have h := Real.one_sub_sq_div_two_lt_cos (by norm_num : (0.58 : ℝ) ≠ 0)
    have h_sq : (0.58 : ℝ) ^ 2 / 2 < (0.17 : ℝ) := by norm_num
    linarith [h, h_sq]
  have h_antitone := Real.antitoneOn_cos
  have h_cos_t_gt_058 : cos (0.58) ≤ cos (arg - pi) :=
    h_antitone h_t_in h058_in (le_of_lt (by simpa [arg] using h_t_hi))
  linarith [h_cos_eq, h_cos_t_gt_058, h_cos_058_gt_083]

lemma dark_energy_exp_factor_gt_five :
    (5 : ℝ) < exp (1 + bleed_in_factor * (1.1 : ℝ)) := by
  have h_bleed : (1.77 : ℝ) < 1 + bleed_in_factor * (1.1 : ℝ) := by
    nlinarith [bleed_in_factor_gt_seven_seven]
  have h_log : log 5 < 1 + bleed_in_factor * (1.1 : ℝ) := lt_trans log_five_lt_one_seven_seven h_bleed
  exact (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 5)).1 h_log

lemma alpha_pos : (0 : ℝ) < alpha := by
  unfold alpha
  exact div_pos (log_pos pi_gt_one)
    (mul_pos (exp_pos _) (pow_pos (lt_trans (by norm_num) phi_gt_one) 13))

lemma growth_term_cosmological_gt_one : (1 : ℝ) < growth_term cosmologicalParams := by
  unfold growth_term cosmologicalParams
  have hφpos : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have h_exp_pos : (0 : ℝ) < alpha * (1 - 0 / 1) * gamma_euler / phi := by
    have h_num : (0 : ℝ) < alpha * gamma_euler := by
      simpa using mul_pos (mul_pos alpha_pos gamma_euler_pos) (by norm_num : (0 : ℝ) < 1)
    simpa [zero_div, sub_zero, mul_one] using div_pos h_num hφpos
  exact one_lt_exp_iff.mpr h_exp_pos

lemma cosmological_growth_coherence_multiplier_gt_one_three_five :
    (1.35 : ℝ) < 1 + growth_term cosmologicalParams * coherence_efficiency := by
  nlinarith [growth_term_cosmological_gt_one, coherence_efficiency_gt_seven_tenths]

lemma sqrt_25_eq_five : sqrt (25 : ℝ) = 5 := by
  rw [sqrt_eq_iff_eq_sq (by norm_num) (by norm_num)]
  norm_num

lemma sqrt_9_eq_3 : sqrt (9 : ℝ) = 3 := by
  rw [sqrt_eq_iff_eq_sq (by norm_num) (by norm_num)]
  norm_num

lemma rpow_pi_pi_gt_27 : (27 : ℝ) < rpow pi pi := by
  have h3lt : (3 : ℝ) < pi := by unfold pi; linarith [pi_gt_d4]
  have h27_pi3 : (27 : ℝ) < pi ^ (3 : ℝ) := by
    rw [show (27 : ℝ) = 3 ^ (3 : ℝ) by norm_num]
    exact rpow_lt_rpow (by norm_num) h3lt (by norm_num : (0 : ℝ) < 3)
  have hpi3_pipi : pi ^ (3 : ℝ) < pi ^ pi :=
    rpow_lt_rpow_of_exponent_lt pi_gt_one (by unfold pi; nlinarith [pi_gt_d4, pi_lt_d4])
  exact lt_trans h27_pi3 hpi3_pipi

lemma e_minus_one_gt_one : (1 : ℝ) < e - 1 := by
  unfold e
  linarith [Real.add_one_lt_exp (by norm_num : (1 : ℝ) ≠ 0)]

lemma beta_exp_exponent_gt_five : (5 : ℝ) < rpow pi pi + (e - 1) := by
  have hpi := rpow_pi_pi_gt_27
  have he := e_minus_one_gt_one
  unfold e at he ⊢
  linarith [hpi, he]

lemma exp_five_gt_100 : (100 : ℝ) < exp 5 := by
  have h : (100 : ℝ) < (2.7 : ℝ) ^ 5 := by norm_num
  have h_e : (2.7 : ℝ) ^ 5 < exp 5 := by
    have h1 : (2.7 : ℝ) < exp 1 := by linarith [exp_one_gt_d9]
    calc (2.7 : ℝ) ^ 5 < (exp 1) ^ 5 := by gcongr
      _ = exp 5 := by rw [← exp_nat_mul]; norm_num
  exact lt_trans h h_e

lemma exp_three_gt_twenty : (20 : ℝ) < exp 3 := by
  have h_poly :
      (20 : ℝ) < 1 + 3 + 3 ^ 2 / 2 + 3 ^ 3 / 6 + 3 ^ 4 / 24 + 3 ^ 5 / 120 + 3 ^ 6 / 720 +
        3 ^ 7 / 5040 + 3 ^ 8 / 40320 + 3 ^ 9 / 362880 + 3 ^ 10 / 3628800 +
        3 ^ 11 / 39916800 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 3) 12
  have h_eq :
      (1 + 3 + 3 ^ 2 / 2 + 3 ^ 3 / 6 + 3 ^ 4 / 24 + 3 ^ 5 / 120 + 3 ^ 6 / 720 + 3 ^ 7 / 5040 +
          3 ^ 8 / 40320 + 3 ^ 9 / 362880 + 3 ^ 10 / 3628800 + 3 ^ 11 / 39916800 : ℝ) =
        ∑ i ∈ Finset.range 12, (3 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma exp_six_gt_400 : (400 : ℝ) < exp 6 := by
  have h_sq : (400 : ℝ) < (exp 3) ^ 2 := by
    nlinarith [exp_three_gt_twenty]
  calc (400 : ℝ) < (exp 3) ^ 2 := h_sq
    _ = exp 3 * exp 3 := by rw [sq]
    _ = exp 6 := by rw [← exp_add, show (6 : ℝ) = 3 + 3 by norm_num]

lemma exp_28_gt_410 : (410 : ℝ) < exp 28 := by
  have h_poly :
      (410 : ℝ) < 1 + 28 + 28 ^ 2 / 2 + 28 ^ 3 / 6 + 28 ^ 4 / 24 + 28 ^ 5 / 120 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 28) 6
  have h_eq :
      (1 + 28 + 28 ^ 2 / 2 + 28 ^ 3 / 6 + 28 ^ 4 / 24 + 28 ^ 5 / 120 : ℝ) =
        ∑ i ∈ Finset.range 6, (28 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma cosmological_N_pos : (0 : ℝ) < cosmologicalParams.N := by
  simp [cosmologicalParams]

lemma cosmological_P_pos : (0 : ℝ) < cosmologicalParams.P := by
  simp [cosmologicalParams]

lemma suction_factor_abs_le_poof : abs suction_factor ≤ poof_factor := by
  dsimp [suction_factor]
  have h_poof_pos : 0 < poof_factor := exp_pos _
  rw [abs_mul, abs_of_nonneg (le_of_lt h_poof_pos), abs_neg]
  nlinarith [abs_cos_le_one (theta_s - pi), h_poof_pos]

lemma phase_variance_abs_le_one : abs phase_variance ≤ 1 := by
  dsimp [phase_variance]
  simp [abs_neg, abs_cos_le_one]

lemma pi_div_e_lt_pi_div_two : pi / e < pi / 2 := by
  unfold e
  have hpi : (0 : ℝ) < pi := Real.pi_pos
  have h_inv : (1 : ℝ) / exp 1 < (1 / 2) :=
    one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < 2) (by linarith [exp_one_gt_d9])
  calc pi / exp 1 = pi * (1 / exp 1) := by ring
    _ < pi * (1 / 2) := mul_lt_mul_of_pos_left h_inv hpi
    _ = pi / 2 := by ring

lemma sin_pi_div_e_lt_one : sin (pi / e) < (1 : ℝ) := by
  have h_pos : (0 : ℝ) < pi / e := div_pos Real.pi_pos (by unfold e; exact exp_pos _)
  have h_lt := pi_div_e_lt_pi_div_two
  have hx : -(pi / 2) ≤ pi / e := by linarith [h_pos]
  have h := sin_lt_sin_of_lt_of_le_pi_div_two hx le_rfl h_lt
  simpa [sin_pi_div_two] using h

lemma one_add_inv_phi_eq_phi : (1 : ℝ) + 1 / phi = phi := by
  unfold phi
  field_simp
  ring_nf
  rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 5)]
  ring

lemma acoustic_bleed_pos : (0 : ℝ) < acoustic_bleed := by
  unfold acoustic_bleed sqrt2
  have hsin : (0 : ℝ) < sin (pi / e) := by
    have h_pos : (0 : ℝ) < pi / e := div_pos Real.pi_pos (by unfold e; exact exp_pos _)
    have h_lt : pi / e < pi := by
      unfold e
      have hpi : (0 : ℝ) < pi := Real.pi_pos
      have h_one : (1 : ℝ) < exp 1 := by linarith [exp_one_gt_d9]
      rw [div_lt_iff₀ (exp_pos _)]
      nlinarith [hpi, h_one]
    exact sin_pos_of_pos_of_lt_pi h_pos h_lt
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have hsqrt : (0 : ℝ) < sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  exact div_pos (mul_pos hsin hφ) hsqrt

lemma acoustic_bleed_lt_phi : acoustic_bleed < phi := by
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have hsin : sin (pi / e) < sqrt 2 :=
    lt_trans sin_pi_div_e_lt_one (Real.lt_sqrt_of_sq_lt (by norm_num))
  have hsqrt_pos : (0 : ℝ) < sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  unfold acoustic_bleed phi sqrt2
  rw [div_lt_iff₀ hsqrt_pos]
  have h := mul_lt_mul_of_pos_right hsin hφ
  simp only [phi] at h ⊢
  rw [mul_comm (sqrt 2) ((1 + sqrt 5) / 2)] at h
  exact h

lemma acoustic_bleed_mul_sin_sq_le_phi :
    acoustic_bleed * (sin 1) ^ 2 ≤ phi := by
  have hsin : (sin 1) ^ 2 ≤ (1 : ℝ) := by
    nlinarith [sin_le_one (1 : ℝ), neg_one_le_sin (1 : ℝ)]
  calc acoustic_bleed * (sin 1) ^ 2
      ≤ acoustic_bleed * 1 := mul_le_mul_of_nonneg_left hsin (le_of_lt acoustic_bleed_pos)
    _ = acoustic_bleed := mul_one _
    _ ≤ phi := le_of_lt acoustic_bleed_lt_phi

lemma acoustic_inflow_pos : (0 : ℝ) < acoustic_inflow := by
  unfold acoustic_inflow
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have h_cos_div : -(1 / phi) ≤ cos theta_s / phi := by
    rw [le_div_iff₀ hφ]
    have h_simp : -(1 / phi) * phi = (-1 : ℝ) := by field_simp [hφ.ne']
    rw [h_simp]
    linarith [neg_one_le_cos theta_s]
  have h_inv_phi : (1 / phi) < (1 : ℝ) := by
    simpa using one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < 1) phi_gt_one
  have h_inner : (0 : ℝ) < 1 + cos theta_s / phi := by linarith [h_cos_div, h_inv_phi]
  exact mul_pos acoustic_bleed_pos h_inner

lemma acoustic_inflow_le_acoustic_bleed_mul_phi :
    acoustic_inflow ≤ acoustic_bleed * phi := by
  unfold acoustic_inflow
  have h_bleed_nonneg : (0 : ℝ) ≤ acoustic_bleed := le_of_lt acoustic_bleed_pos
  have hcos := div_le_div_of_nonneg_right (cos_le_one theta_s) (le_of_lt (lt_trans (by norm_num) phi_gt_one))
  have h_inner : (1 : ℝ) + cos theta_s / phi ≤ phi := by
    have h := hcos
    linarith [one_add_inv_phi_eq_phi]
  exact mul_le_mul_of_nonneg_left h_inner h_bleed_nonneg

lemma cos_one_sq_le : (cos 1) ^ 2 ≤ (25 : ℝ) / 81 := by
  nlinarith [cos_one_le, cos_one_pos.le, sq_nonneg (5 / 9)]

lemma acoustic_inflow_mul_cos_sq_le_phi :
    acoustic_inflow * (cos 1) ^ 2 ≤ phi := by
  have h1 := acoustic_inflow_le_acoustic_bleed_mul_phi
  have hcos := cos_one_sq_le
  have h_bleed := le_of_lt acoustic_bleed_lt_phi
  have hφpos : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have hprod_nonneg : (0 : ℝ) ≤ acoustic_bleed * phi := mul_nonneg (le_of_lt acoustic_bleed_pos) (le_of_lt hφpos)
  calc acoustic_inflow * (cos 1) ^ 2
      ≤ acoustic_bleed * phi * (cos 1) ^ 2 := by
        simpa [mul_assoc] using mul_le_mul_of_nonneg_right h1 (sq_nonneg (cos 1))
    _ ≤ acoustic_bleed * phi * (25 / 81) := mul_le_mul_of_nonneg_left hcos hprod_nonneg
    _ ≤ phi * phi * (25 / 81) := by
        have hpp : acoustic_bleed * phi ≤ phi * phi := by nlinarith [h_bleed, hφpos]
        exact mul_le_mul_of_nonneg_right hpp (by norm_num : (0 : ℝ) ≤ 25 / 81)
    _ ≤ phi := by nlinarith [phi_gt_one, phi_lt_two]

/-! ### Wave 1 interval certificates (aligned with `canonical_constants.json`) -/

lemma e_gt_27182818283 : (2.7182818283 : ℝ) < e := by
  unfold e; linarith [exp_one_gt_d9]

lemma e_lt_27182818286 : e < (2.7182818286 : ℝ) := by
  unfold e; linarith [exp_one_lt_d9]

lemma pi_gt_314159265358979323846 : (3.14159265358979323846 : ℝ) < pi := by
  unfold pi; exact pi_gt_d20

lemma pi_lt_314159265358979323847 : pi < (3.14159265358979323847 : ℝ) := by
  unfold pi; exact pi_lt_d20

lemma e_pi_gt_27182818283_mul_pi :
    (2.7182818283 : ℝ) * (3.14159265358979323846 : ℝ) < e * pi := by
  have hp_pos : (0 : ℝ) < pi := by unfold pi; linarith [pi_gt_d20]
  exact mul_lt_mul_of_pos e_gt_27182818283 pi_gt_314159265358979323846
    (by norm_num : (0 : ℝ) < (2.7182818283 : ℝ)) hp_pos

lemma e_pi_lt_27182818286_mul_pi :
    e * pi < (2.7182818286 : ℝ) * (3.14159265358979323847 : ℝ) := by
  have he_pos : (0 : ℝ) < e := by unfold e; exact exp_pos 1
  exact mul_lt_mul_of_pos e_lt_27182818286 pi_lt_314159265358979323847 he_pos
    (by norm_num : (0 : ℝ) < (3.14159265358979323847 : ℝ))

lemma e_pi_gt_85397323 : (85397323 : ℝ) / 10000000 < e * pi := by
  have hp_pos : (0 : ℝ) < pi := by unfold pi; linarith [pi_gt_d20]
  have hmul : (2.7182818283 : ℝ) * (3.14159265358979323846 : ℝ) < e * pi :=
    mul_lt_mul_of_pos e_gt_27182818283 pi_gt_314159265358979323846
      (by norm_num : (0 : ℝ) < (2.7182818283 : ℝ)) hp_pos
  have hconst : (85397323 : ℝ) / 10000000 < (2.7182818283 : ℝ) * (3.14159265358979323846 : ℝ) := by norm_num
  linarith [hmul, hconst]

lemma e_pi_gt_8539732 : (8539732 : ℝ) / 1000000 < e * pi := by
  have hp_pos : (0 : ℝ) < pi := by unfold pi; linarith [pi_gt_d20]
  have hmul : (2.7182818283 : ℝ) * (3.14159265358979323846 : ℝ) < e * pi :=
    mul_lt_mul_of_pos e_gt_27182818283 pi_gt_314159265358979323846
      (by norm_num : (0 : ℝ) < (2.7182818283 : ℝ)) hp_pos
  have hconst : (8539732 : ℝ) / 1000000 < (2.7182818283 : ℝ) * (3.14159265358979323846 : ℝ) := by norm_num
  linarith [hmul, hconst]

lemma e_pi_lt_853973478 : e * pi < (853973478 : ℝ) / 100000000 := by
  have he_pos : (0 : ℝ) < e := by unfold e; exact exp_pos 1
  have hmul : e * pi < (2.7182818286 : ℝ) * (3.14159265358979323847 : ℝ) :=
    mul_lt_mul_of_pos e_lt_27182818286 pi_lt_314159265358979323847 he_pos
      (by norm_num : (0 : ℝ) < (3.14159265358979323847 : ℝ))
  have hconst : (2.7182818286 : ℝ) * (3.14159265358979323847 : ℝ) < (853973478 : ℝ) / 100000000 := by norm_num
  linarith [hmul, hconst]

lemma e_pi_lt_85397348 : e * pi < (85397348 : ℝ) / 10000000 := by
  have he_pos : (0 : ℝ) < e := by unfold e; exact exp_pos 1
  have hmul : e * pi < (2.7182818286 : ℝ) * (3.14159265358979323847 : ℝ) :=
    mul_lt_mul_of_pos e_lt_27182818286 pi_lt_314159265358979323847 he_pos
      (by norm_num : (0 : ℝ) < (3.14159265358979323847 : ℝ))
  have hconst : (2.7182818286 : ℝ) * (3.14159265358979323847 : ℝ) < (85397348 : ℝ) / 10000000 := by norm_num
  linarith [hmul, hconst]

lemma e_pi_lt_8539736 : e * pi < (8539736 : ℝ) / 1000000 := by
  have he_pos : (0 : ℝ) < e := by unfold e; exact exp_pos 1
  have hmul : e * pi < (2.7182818286 : ℝ) * (3.14159265358979323847 : ℝ) :=
    mul_lt_mul_of_pos e_lt_27182818286 pi_lt_314159265358979323847 he_pos
      (by norm_num : (0 : ℝ) < (3.14159265358979323847 : ℝ))
  have hconst : (2.7182818286 : ℝ) * (3.14159265358979323847 : ℝ) < (8539736 : ℝ) / 1000000 := by norm_num
  linarith [hmul, hconst]

lemma sqrt2_gt_14142135623 : (1.4142135623 : ℝ) < sqrt2 := by
  unfold sqrt2
  exact Real.lt_sqrt_of_sq_lt (by norm_num)

lemma sqrt2_lt_14142135624 : sqrt2 < (1.4142135624 : ℝ) := by
  unfold sqrt2
  exact sqrt_two_lt_14142135624

lemma sin_bound_lo {x : ℝ} (hx : |x| ≤ 1) :
    x - x ^ 3 / 6 - |x| ^ 4 * (5 / 96) ≤ sin x := by
  have := (abs_le.mp (Real.sin_bound hx)).1
  linarith

lemma sin_bound_hi {x : ℝ} (hx : |x| ≤ 1) :
    sin x ≤ x - x ^ 3 / 6 + |x| ^ 4 * (5 / 96) := by
  have := (abs_le.mp (Real.sin_bound hx)).2
  linarith

lemma cos_bound_lo {x : ℝ} (hx : |x| ≤ 1) :
    1 - x ^ 2 / 2 - |x| ^ 4 * (5 / 96) ≤ cos x := by
  have := (abs_le.mp (Real.cos_bound hx)).1
  linarith

lemma cos_bound_hi {x : ℝ} (hx : |x| ≤ 1) :
    cos x ≤ 1 - x ^ 2 / 2 + |x| ^ 4 * (5 / 96) := by
  have := (abs_le.mp (Real.cos_bound hx)).2
  linarith

lemma pi_half_gt_02956 : (0.295612 : ℝ) < pi / 2 := by
  unfold pi
  nlinarith [pi_gt_d4]

lemma pi_half_gt_1156 : (1.15572734986 : ℝ) < pi / 2 := by
  unfold pi
  nlinarith [pi_gt_d4]

lemma neg_pi_half_le_zero : -(pi / 2) ≤ (0 : ℝ) := by
  unfold pi
  nlinarith [Real.pi_pos]

lemma pi_gt_290272 : (0.290272 : ℝ) < pi := by
  unfold pi
  nlinarith [pi_gt_d4]

lemma pi_gt_291325 : (0.291325 : ℝ) < pi := by
  unfold pi
  nlinarith [pi_gt_d4]

lemma pi_gt_0415068 : (0.415068 : ℝ) < pi := by
  unfold pi
  nlinarith [pi_gt_d4]

lemma pi_gt_0415069 : (0.415069 : ℝ) < pi := by
  unfold pi
  nlinarith [pi_gt_d4]

lemma psi_con_gt_6321205588 : (0.6321205588 : ℝ) < psi_con := by
  unfold psi_con
  linarith [Real.exp_neg_one_lt_d9]

lemma psi_con_lt_63212055884 : psi_con < (0.63212055884 : ℝ) := by
  unfold psi_con
  linarith [Real.exp_neg_one_gt_d9]

lemma eta_eff_gt_466942206 : (0.466942206 : ℝ) < eta_eff := by
  unfold eta_eff
  have hsub : pi - 1 < (2.14159265358979323847 : ℝ) := by
    linarith [pi_lt_314159265358979323847]
  have hone : (1 / (2.14159265358979323847 : ℝ)) < 1 / (pi - 1) :=
    one_div_lt_one_div_of_lt pi_sub_one_pos hsub
  have hnum : (0.466942206 : ℝ) < 1 / (2.14159265358979323847 : ℝ) := by norm_num
  linarith

lemma eta_eff_lt_466942299692 : eta_eff < (0.466942299692 : ℝ) := by
  unfold eta_eff
  have hsub : (2.14159265358979323846 : ℝ) < pi - 1 := by
    linarith [pi_gt_314159265358979323846]
  have hone : 1 / (pi - 1) < 1 / (2.14159265358979323846 : ℝ) :=
    one_div_lt_one_div_of_lt (by linarith [pi_sub_one_pos]) hsub
  have hnum : 1 / (2.14159265358979323846 : ℝ) < (0.466942299692 : ℝ) := by norm_num
  linarith

lemma psi_con_eta_prod_gt_295163 : (0.295163 : ℝ) < psi_con * eta_eff := by
  have h_const : (0.295163 : ℝ) < (0.6321205588 : ℝ) * (0.466942206 : ℝ) := by norm_num
  nlinarith [psi_con_gt_6321205588, eta_eff_gt_466942206, h_const, psi_con_pos, eta_pos]

lemma psi_con_eta_prod_lt_295164 : psi_con * eta_eff < (0.295164 : ℝ) := by
  have h_const : (0.63212055884 : ℝ) * (0.466942299692 : ℝ) < (0.295164 : ℝ) := by norm_num
  nlinarith [psi_con_lt_63212055884, eta_eff_lt_466942299692, h_const, psi_con_pos, eta_pos]

lemma psi_con_eta_in_Icc_sin : psi_con * eta_eff ∈ Set.Icc (-(pi / 2)) (pi / 2) := by
  constructor
  · linarith [psi_con_eta_prod_gt_295163, neg_pi_half_le_zero]
  · exact le_of_lt (lt_trans psi_con_eta_prod_lt_295164
      (lt_trans (by norm_num : (0.295164 : ℝ) < (0.295612 : ℝ)) pi_half_gt_02956))

lemma sin_0295163_gt_0290272 : (0.290272 : ℝ) < sin (0.295163 : ℝ) := by
  have h := sin_bound_lo (by norm_num : |(0.295163 : ℝ)| ≤ 1)
  have h_num :
      (0.290272 : ℝ) <
        (0.295163 : ℝ) - (0.295163 : ℝ) ^ 3 / 6 - (0.295163 : ℝ) ^ 4 * (5 / 96) := by
    norm_num
  linarith [h, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ (0.295163 : ℝ))]

lemma sin_0295164_lt_0291325 : sin (0.295164 : ℝ) < (0.291325 : ℝ) := by
  have h := sin_bound_hi (by norm_num : |(0.295164 : ℝ)| ≤ 1)
  have h_num :
      (0.295164 : ℝ) - (0.295164 : ℝ) ^ 3 / 6 + (0.295164 : ℝ) ^ 4 * (5 / 96) <
        (0.291325 : ℝ) := by
    norm_num
  linarith [h, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ (0.295164 : ℝ))]

lemma theta_s_gt_290272 : (0.290272 : ℝ) < theta_s := by
  unfold theta_s
  have h_prod_lo := psi_con_eta_prod_gt_295163
  have h_icc_a : (0.295163 : ℝ) ∈ Set.Icc (-(pi / 2)) (pi / 2) := by
    constructor
    · linarith [neg_pi_half_le_zero]
    · exact le_of_lt (lt_trans (by norm_num : (0.295163 : ℝ) < (0.295612 : ℝ)) pi_half_gt_02956)
  have h_icc_b := psi_con_eta_in_Icc_sin
  exact lt_trans sin_0295163_gt_0290272 (strictMonoOn_sin h_icc_a h_icc_b h_prod_lo)

lemma theta_s_lt_291325 : theta_s < (0.291325 : ℝ) := by
  unfold theta_s
  have h_prod_hi := psi_con_eta_prod_lt_295164
  have h_icc_a := psi_con_eta_in_Icc_sin
  have h_icc_b : (0.295164 : ℝ) ∈ Set.Icc (-(pi / 2)) (pi / 2) := by
    constructor
    · linarith [neg_pi_half_le_zero]
    · exact le_of_lt (lt_trans (by norm_num : (0.295164 : ℝ) < (0.295612 : ℝ)) pi_half_gt_02956)
  exact lt_trans (strictMonoOn_sin h_icc_a h_icc_b h_prod_hi) sin_0295164_lt_0291325

lemma pi_div_e_gt_115572734973 : (1.15572734973 : ℝ) < pi / e := by
  rw [lt_div_iff₀ (by unfold e; exact exp_pos _)]
  nlinarith [pi_gt_314159265358979323846, e_lt_27182818286]

lemma pi_div_e_lt_115572734986 : pi / e < (1.15572734986 : ℝ) := by
  rw [div_lt_iff₀ (by unfold e; exact exp_pos _)]
  nlinarith [pi_lt_314159265358979323847, e_gt_27182818283]

lemma pi_div_e_in_Icc_sin : pi / e ∈ Set.Icc (-(pi / 2)) (pi / 2) := by
  constructor
  · linarith [pi_div_e_gt_115572734973, neg_pi_half_le_zero]
  · exact le_of_lt (lt_trans pi_div_e_lt_115572734986 pi_half_gt_1156)

lemma sin_eq_cos_pi_div_two_sub (x : ℝ) : sin x = cos (pi / 2 - x) := by
  simpa [pi_eq_real_pi] using (cos_pi_div_two_sub x).symm

lemma cos_eq_sin_pi_div_two_sub (x : ℝ) : cos x = sin (pi / 2 - x) := by
  calc
    cos x = cos (pi / 2 - (pi / 2 - x)) := by congr 1; ring
    _ = sin (pi / 2 - x) := (sin_eq_cos_pi_div_two_sub (pi / 2 - x)).symm

lemma cos_0415069_gt_091385 : (0.91385 : ℝ) < cos (0.415069 : ℝ) := by
  have h := one_sub_sq_div_two_le_cos (x := (0.415069 : ℝ))
  have h_num : (0.91385 : ℝ) < 1 - (0.415069 : ℝ) ^ 2 / 2 := by norm_num
  linarith

lemma cos_0415068_lt_091541 : cos (0.415068 : ℝ) < (0.91541 : ℝ) := by
  have h := cos_bound_hi (by norm_num : |(0.415068 : ℝ)| ≤ 1)
  have h_num :
      1 - (0.415068 : ℝ) ^ 2 / 2 + (0.415068 : ℝ) ^ 4 * (5 / 96) < (0.91541 : ℝ) := by
    norm_num
  linarith [h, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ (0.415068 : ℝ))]

lemma sin_pi_div_e_gt_91385 : (0.91385 : ℝ) < sin (pi / e) := by
  have h_half_hi : pi / e < pi / 2 :=
    lt_trans pi_div_e_lt_115572734986 pi_half_gt_1156
  have h_y_hi : pi / 2 - pi / e < (0.415069 : ℝ) := by
    nlinarith [pi_div_e_gt_115572734973, pi_gt_314159265358979323846,
      pi_lt_314159265358979323847]
  have h_cos : (0.91385 : ℝ) < cos (pi / 2 - pi / e) := by
    have h_ref : (0.415069 : ℝ) ∈ Set.Icc (0 : ℝ) pi := ⟨by norm_num, le_of_lt pi_gt_0415069⟩
    have h_y : pi / 2 - pi / e ∈ Set.Icc (0 : ℝ) pi := by
      constructor
      · linarith [h_y_hi]
      · have hlt : pi / 2 - pi / e < pi / 2 := by linarith [pi_div_e_gt_115572734973]
        exact le_of_lt (lt_trans hlt (half_lt_self (by unfold pi; linarith [Real.pi_pos])))
    exact lt_trans cos_0415069_gt_091385 (strictAntiOn_cos h_y h_ref h_y_hi)
  simpa [sin_eq_cos_pi_div_two_sub] using h_cos

lemma sin_pi_div_e_lt_91541 : sin (pi / e) < (0.91541 : ℝ) := by
  have h_half_hi : pi / e < pi / 2 :=
    lt_trans pi_div_e_lt_115572734986 pi_half_gt_1156
  have h_y_lo : (0.415068 : ℝ) < pi / 2 - pi / e := by
    nlinarith [pi_div_e_lt_115572734986, pi_gt_314159265358979323846,
      pi_lt_314159265358979323847]
  have h_cos : cos (pi / 2 - pi / e) < (0.91541 : ℝ) := by
    have h_ref : (0.415068 : ℝ) ∈ Set.Icc (0 : ℝ) pi := ⟨by norm_num, le_of_lt pi_gt_0415068⟩
    have h_y : pi / 2 - pi / e ∈ Set.Icc (0 : ℝ) pi := by
      constructor
      · linarith [h_y_lo]
      · have hlt : pi / 2 - pi / e < pi / 2 := by linarith [pi_div_e_gt_115572734973]
        exact le_of_lt (lt_trans hlt (half_lt_self (by unfold pi; linarith [Real.pi_pos])))
    exact lt_trans (strictAntiOn_cos h_ref h_y h_y_lo) cos_0415068_lt_091541
  simpa [sin_eq_cos_pi_div_two_sub] using h_cos

lemma acoustic_bleed_gt_10455 : (1.0455 : ℝ) < acoustic_bleed := by
  unfold acoustic_bleed
  have hsin := sin_pi_div_e_gt_91385
  have hφ := phi_gt_1618
  have hsqrt := sqrt2_lt_14142135624
  have hsqrt_pos : (0 : ℝ) < sqrt2 := by unfold sqrt2; exact Real.sqrt_pos.mpr (by norm_num)
  have h_mid : (1.0455 : ℝ) * (1.4142135624 : ℝ) < (0.91385 : ℝ) * (1.618 : ℝ) := by norm_num
  have h_prod : (1.0455 : ℝ) * sqrt2 < sin (pi / e) * phi := by
    have h1 : (1.0455 : ℝ) * sqrt2 < (1.0455 : ℝ) * (1.4142135624 : ℝ) := by nlinarith [hsqrt]
    nlinarith [hsin, hφ, h1, h_mid]
  exact (lt_div_iff₀ hsqrt_pos).mpr h_prod

lemma acoustic_bleed_lt_10476 : acoustic_bleed < (1.0476 : ℝ) := by
  unfold acoustic_bleed
  have hsin := sin_pi_div_e_lt_91541
  have hφ := phi_lt_16181
  have hsqrt := sqrt2_gt_14142135623
  have hsqrt_pos : (0 : ℝ) < sqrt2 := by unfold sqrt2; exact Real.sqrt_pos.mpr (by norm_num)
  have h_mid : (0.91541 : ℝ) * (1.6181 : ℝ) < (1.0476 : ℝ) * (1.4142135623 : ℝ) := by norm_num
  have h_prod : sin (pi / e) * phi < (1.0476 : ℝ) * sqrt2 := by
    have h1 : sin (pi / e) * phi < (0.91541 : ℝ) * (1.6181 : ℝ) :=
      mul_lt_mul_of_pos hsin hφ (by linarith [sin_pi_div_e_gt_91385]) (by norm_num : (0 : ℝ) < 1.6181)
    have h2 : (1.0476 : ℝ) * (1.4142135623 : ℝ) < (1.0476 : ℝ) * sqrt2 := by nlinarith [hsqrt]
    linarith [h1, h_mid, h2]
  exact (div_lt_iff₀ hsqrt_pos).mpr h_prod

lemma theta_s_in_Icc_cos : theta_s ∈ Set.Icc (0 : ℝ) pi := by
  constructor
  · exact le_of_lt (lt_trans (by norm_num) theta_s_gt_290272)
  · exact le_of_lt (lt_trans theta_s_lt_291325 pi_gt_291325)

lemma cos_0290272_lt_095825 : cos (0.290272 : ℝ) < (0.95825 : ℝ) := by
  have h := cos_bound_hi (by norm_num : |(0.290272 : ℝ)| ≤ 1)
  have h_num :
      1 - (0.290272 : ℝ) ^ 2 / 2 + (0.290272 : ℝ) ^ 4 * (5 / 96) < (0.95825 : ℝ) := by
    norm_num
  linarith [h, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ (0.290272 : ℝ))]

lemma cos_0291325_gt_09575 : (0.9575 : ℝ) < cos (0.291325 : ℝ) := by
  have h := one_sub_sq_div_two_le_cos (x := (0.291325 : ℝ))
  have h_num : (0.9575 : ℝ) < 1 - (0.291325 : ℝ) ^ 2 / 2 := by norm_num
  linarith

lemma cos_theta_s_gt_09575 : (0.9575 : ℝ) < cos theta_s := by
  have hθ := theta_s_lt_291325
  have h_ref : (0.291325 : ℝ) ∈ Set.Icc (0 : ℝ) pi :=
    ⟨by norm_num, le_of_lt pi_gt_291325⟩
  exact lt_trans cos_0291325_gt_09575 (strictAntiOn_cos theta_s_in_Icc_cos h_ref hθ)

lemma cos_theta_s_lt_095825 : cos theta_s < (0.95825 : ℝ) := by
  have hθ := theta_s_gt_290272
  have h_ref : (0.290272 : ℝ) ∈ Set.Icc (0 : ℝ) pi :=
    ⟨by norm_num, le_of_lt pi_gt_290272⟩
  exact lt_trans (strictAntiOn_cos h_ref theta_s_in_Icc_cos hθ) cos_0290272_lt_095825

lemma acoustic_inflow_gt_16639 : (1.6639 : ℝ) < acoustic_inflow := by
  unfold acoustic_inflow
  have h_bleed := acoustic_bleed_gt_10455
  have h_cos := cos_theta_s_gt_09575
  have hφ := phi_lt_16181
  have h_div_lo : (0.5915 : ℝ) < cos theta_s / phi := by
    rw [lt_div_iff₀ (lt_trans (by norm_num) phi_gt_one)]
    nlinarith [h_cos, hφ]
  have h_inner_lo : (1.5915 : ℝ) < 1 + cos theta_s / phi := by linarith [h_div_lo]
  have h_const : (1.6639 : ℝ) < (1.0455 : ℝ) * (1.5915 : ℝ) := by norm_num
  have h_prod : (1.0455 : ℝ) * (1.5915 : ℝ) < acoustic_bleed * (1 + cos theta_s / phi) := by
    nlinarith [h_bleed, h_inner_lo]
  linarith [h_const, h_prod]

lemma acoustic_inflow_lt_16695 : acoustic_inflow < (1.6695 : ℝ) := by
  unfold acoustic_inflow
  have h_bleed := acoustic_bleed_lt_10476
  have h_cos := cos_theta_s_lt_095825
  have hφ := phi_gt_1618
  have h_div_hi : cos theta_s / phi < (0.5923 : ℝ) := by
    rw [div_lt_iff₀ (lt_trans (by norm_num) phi_gt_one)]
    nlinarith [h_cos, hφ]
  have h_inner_hi : 1 + cos theta_s / phi < (1.5923 : ℝ) := by linarith [h_div_hi]
  have h_const : (1.0476 : ℝ) * (1.5923 : ℝ) < (1.6695 : ℝ) := by norm_num
  have h_bleed_pos : (0 : ℝ) < acoustic_bleed := by
    unfold acoustic_bleed
    apply div_pos
    · exact mul_pos (by linarith [sin_pi_div_e_gt_91385]) (by linarith [phi_gt_1618])
    · unfold sqrt2; exact Real.sqrt_pos.mpr (by norm_num)
  have h_inner_pos : (0 : ℝ) < 1 + cos theta_s / phi := by
    have hcos : (0 : ℝ) < cos theta_s := by linarith [cos_theta_s_gt_09575]
    have hφpos : (0 : ℝ) < phi := by linarith [phi_gt_1618]
    linarith [div_pos hcos hφpos]
  have h_prod : acoustic_bleed * (1 + cos theta_s / phi) < (1.0476 : ℝ) * (1.5923 : ℝ) :=
    mul_lt_mul_of_pos h_bleed h_inner_hi h_bleed_pos (by norm_num : (0 : ℝ) < 1.5923)
  linarith [h_prod, h_const]

lemma acoustic_bleed_div_inflow_gt_62600 : (0.62600 : ℝ) < acoustic_bleed / acoustic_inflow := by
  have h : (0.62600 : ℝ) * acoustic_inflow < acoustic_bleed := by
    have h_const : (0.62600 : ℝ) * (1.6695 : ℝ) < (1.0455 : ℝ) := by norm_num
    nlinarith [acoustic_bleed_gt_10455, acoustic_inflow_lt_16695, h_const]
  exact (lt_div_iff₀ acoustic_inflow_pos).2 h

lemma acoustic_bleed_div_inflow_lt_62961 : acoustic_bleed / acoustic_inflow < (0.62961 : ℝ) := by
  have h_prod : acoustic_bleed < (0.62961 : ℝ) * acoustic_inflow := by
    have h_mid : (1.0476 : ℝ) < (0.62961 : ℝ) * (1.6639 : ℝ) := by norm_num
    have h_scale : (0.62961 : ℝ) * (1.6639 : ℝ) ≤ (0.62961 : ℝ) * acoustic_inflow := by
      gcongr
      exact le_of_lt acoustic_inflow_gt_16639
    linarith [acoustic_bleed_lt_10476, h_mid, h_scale]
  exact (div_lt_iff₀ acoustic_inflow_pos).2 h_prod

lemma phi_sq_gt_261792 : (2.617924 : ℝ) < phi ^ 2 := by
  nlinarith [phi_gt_1618]

lemma phi_sq_lt_26183 : phi ^ 2 < (26183 : ℝ) / 10000 := by
  have hφ : phi < (16181 : ℝ) / 10000 := by linarith [phi_lt_16181]
  have hsq : phi ^ 2 < ((16181 : ℝ) / 10000) ^ 2 :=
    pow_lt_pow_left₀ hφ (le_of_lt (lt_trans (by norm_num) phi_gt_one)) (by norm_num : (2 : ℕ) ≠ 0)
  have hsq' : phi ^ 2 < (16181 : ℝ) ^ 2 / 10000 ^ 2 := by simpa [div_pow] using hsq
  have hconst : (16181 : ℝ) ^ 2 / 10000 ^ 2 < (26183 : ℝ) / 10000 := by
    simp only [pow_two]
    norm_num
  exact lt_trans hsq' hconst

lemma one_div_pi_gt_03183 : (0.3183 : ℝ) < 1 / pi := by
  rw [lt_div_iff₀ (by unfold pi; linarith [pi_gt_d20])]
  nlinarith [pi_lt_314159265358979323847]

lemma one_div_pi_lt_03184 : 1 / pi < (0.3184 : ℝ) := by
  rw [div_lt_iff₀ (by unfold pi; linarith [pi_gt_d20])]
  nlinarith [pi_gt_314159265358979323846]

lemma exp_04807_lt_1618 : exp 0.4807 < (1.618 : ℝ) := by
  have h := Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.4807) (by norm_num : (0.4807 : ℝ) ≤ 1)
    (by norm_num : (0 : ℕ) < 10)
  have h_sum_lt :
      (∑ m ∈ Finset.range 10, (0.4807 : ℝ) ^ m / m.factorial) +
          (0.4807 : ℝ) ^ 10 * (10 + 1) / (Nat.factorial 10 * 10) <
        (1.618 : ℝ) := by
    norm_num [Finset.range, Nat.factorial]
  exact lt_of_le_of_lt h h_sum_lt

lemma log_1618_gt_04807 : (0.4807 : ℝ) < log (1.618 : ℝ) :=
  (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 1.618)).2 exp_04807_lt_1618

lemma exp_01530_gt_11653 : (1.1653 : ℝ) < exp 0.1530 := by
  have h_poly :
      (1.1653 : ℝ) <
        1 + (0.1530 : ℝ) + (0.1530 : ℝ) ^ 2 / 2 + (0.1530 : ℝ) ^ 3 / 6 +
          (0.1530 : ℝ) ^ 4 / 24 := by
    norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 0.1530) 5
  have h_eq :
      (1 + (0.1530 : ℝ) + (0.1530 : ℝ) ^ 2 / 2 + (0.1530 : ℝ) ^ 3 / 6 +
          (0.1530 : ℝ) ^ 4 / 24 : ℝ) =
        ∑ i ∈ Finset.range 5, (0.1530 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma exp_01534_lt_1168 : exp 0.1534 < (1.168 : ℝ) := by
  have h := Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.1534) (by norm_num : (0.1534 : ℝ) ≤ 1)
    (by norm_num : (0 : ℕ) < 3)
  have h_sum_lt :
      (∑ m ∈ Finset.range 3, (0.1534 : ℝ) ^ m / m.factorial) +
          (0.1534 : ℝ) ^ 3 * (3 + 1) / (Nat.factorial 3 * 3) <
        (1.168 : ℝ) := by
    norm_num [Finset.range, Nat.factorial]
  exact lt_of_le_of_lt h h_sum_lt

lemma phi_rpow_inv_pi_gt_11653 : (1.1653 : ℝ) < phi ^ (1 / pi) := by
  have h_base : (1.618 : ℝ) ^ (1 / pi) < phi ^ (1 / pi) :=
    Real.rpow_lt_rpow (by norm_num) phi_gt_1618 (by linarith [one_div_pi_gt_03183])
  have h_const : (1.1653 : ℝ) < (1.618 : ℝ) ^ (1 / pi) := by
    rw [Real.rpow_def_of_pos (by norm_num), mul_comm]
    have h_arg : (0.1530 : ℝ) < (1 / pi) * log (1.618 : ℝ) := by
      nlinarith [log_1618_gt_04807, one_div_pi_gt_03183]
    exact lt_trans exp_01530_gt_11653 (exp_lt_exp.mpr h_arg)
  exact lt_trans h_const h_base

lemma phi_rpow_inv_pi_lt_1168 : phi ^ (1 / pi) < (1.168 : ℝ) := by
  have h_base : phi ^ (1 / pi) < (1.6181 : ℝ) ^ (1 / pi) :=
    Real.rpow_lt_rpow (le_of_lt (lt_trans (by norm_num) phi_gt_one)) phi_lt_16181
      (by linarith [one_div_pi_gt_03183])
  have h_const : (1.6181 : ℝ) ^ (1 / pi) < (1.168 : ℝ) := by
    rw [Real.rpow_def_of_pos (by norm_num), mul_comm]
    have h_log_pos : (0 : ℝ) < log (1.6181 : ℝ) := log_pos (by norm_num)
    have h_arg : (1 / pi) * log (1.6181 : ℝ) < (0.1534 : ℝ) := by
      have h1 : (1 / pi) * log (1.6181 : ℝ) < (0.3184 : ℝ) * log (1.6181 : ℝ) :=
        mul_lt_mul_of_pos_right one_div_pi_lt_03184 h_log_pos
      have h2 : (0.3184 : ℝ) * log (1.6181 : ℝ) < (0.3184 : ℝ) * (0.4813 : ℝ) :=
        mul_lt_mul_of_pos_left log_16181_lt_04813 (by norm_num)
      have h3 : (0.3184 : ℝ) * (0.4813 : ℝ) < (0.1534 : ℝ) := by norm_num
      linarith [h1, h2, h3]
    exact lt_trans (exp_lt_exp.mpr h_arg) exp_01534_lt_1168
  exact lt_trans h_base h_const

/-! ### Domain sign-proof interval certificates -/

lemma phase_variance_eq_cos_theta_s : phase_variance = cos theta_s := by
  unfold phase_variance
  simp only [pi_eq_real_pi]
  rw [cos_add_pi, neg_neg]

lemma phase_variance_gt_0955 : (0.955 : ℝ) < phase_variance := by
  rw [phase_variance_eq_cos_theta_s]
  linarith [cos_theta_s_gt_09575]

lemma phase_variance_lt_0961 : phase_variance < (0.961 : ℝ) := by
  rw [phase_variance_eq_cos_theta_s]
  linarith [cos_theta_s_lt_095825]

lemma exp_1146_gt_31416 : (3.1416 : ℝ) < exp 1.146 := by
  have h_poly :
      (3.1416 : ℝ) < 1 + (1.146 : ℝ) + (1.146 : ℝ) ^ 2 / 2 + (1.146 : ℝ) ^ 3 / 6 +
        (1.146 : ℝ) ^ 4 / 24 + (1.146 : ℝ) ^ 5 / 120 + (1.146 : ℝ) ^ 6 / 720 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 1.146) 7
  have h_eq :
      (1 + (1.146 : ℝ) + (1.146 : ℝ) ^ 2 / 2 + (1.146 : ℝ) ^ 3 / 6 + (1.146 : ℝ) ^ 4 / 24 +
          (1.146 : ℝ) ^ 5 / 120 + (1.146 : ℝ) ^ 6 / 720 : ℝ) =
        ∑ i ∈ Finset.range 7, (1.146 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma log_31416_lt_1146 : log (3.1416 : ℝ) < (1.146 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < (3.1416 : ℝ))).2 exp_1146_gt_31416

lemma log_pi_lt_1146 : log pi < (1.146 : ℝ) := by
  have hpi : pi < (3.1416 : ℝ) := by unfold pi; exact pi_lt_d4
  exact lt_trans (log_lt_log (lt_trans (by norm_num) pi_gt_one) hpi) log_31416_lt_1146

lemma exp_11453_gt_pi23847 : (3.14159265358979323847 : ℝ) < exp (1.1453 : ℝ) := by
  have h_poly :
      (3.14159265358979323847 : ℝ) < 1 + (1.1453 : ℝ) + (1.1453 : ℝ) ^ 2 / 2 +
        (1.1453 : ℝ) ^ 3 / 6 + (1.1453 : ℝ) ^ 4 / 24 + (1.1453 : ℝ) ^ 5 / 120 +
        (1.1453 : ℝ) ^ 6 / 720 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 1.1453) 7
  have h_eq :
      (1 + (1.1453 : ℝ) + (1.1453 : ℝ) ^ 2 / 2 + (1.1453 : ℝ) ^ 3 / 6 +
          (1.1453 : ℝ) ^ 4 / 24 + (1.1453 : ℝ) ^ 5 / 120 + (1.1453 : ℝ) ^ 6 / 720 : ℝ) =
        ∑ i ∈ Finset.range 7, (1.1453 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma log_pi23847_lt_11453 : log (3.14159265358979323847 : ℝ) < (1.1453 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < (3.14159265358979323847 : ℝ))).2 exp_11453_gt_pi23847

lemma log_pi_lt_11453 : log pi < (1.1453 : ℝ) := by
  have hpi : pi < (3.14159265358979323847 : ℝ) := by unfold pi; exact pi_lt_d20
  exact lt_trans (log_lt_log (lt_trans (by norm_num) pi_gt_one) hpi) log_pi23847_lt_11453

lemma log_pi_div_e_lt_422 : log pi / e < (0.422 : ℝ) := by
  unfold e
  rw [div_lt_iff₀ (exp_pos 1)]
  nlinarith [log_pi_lt_1146, exp_one_gt_d9]

lemma k_gt_0420 : (0.42 : ℝ) < k := by
  unfold k
  have h_log_pos : (0 : ℝ) < log pi := log_pos pi_gt_one
  have h99_pos : (0 : ℝ) < (99 / 100 : ℝ) := by norm_num
  have h_den : (0.42 : ℝ) * log pi < phi * new_perceived_param * (99 / 100) := by
    have h_np := new_perceived_param_gt_30030
    have h_phi := phi_gt_1618
    nlinarith [h_np, h_phi, new_perceived_param_pos, log_pi_lt_11453]
  have h_step1 : (0.42 : ℝ) * log pi / (99 / 100) < phi * new_perceived_param :=
    (div_lt_iff₀ h99_pos).mpr h_den
  have h_step2 : (0.42 : ℝ) / (99 / 100) < phi * new_perceived_param / log pi := by
    have h := div_lt_div_of_pos_right h_step1 h_log_pos
    have h_lhs : (0.42 : ℝ) * log pi / (99 / 100) / log pi = (0.42 : ℝ) / (99 / 100) := by field_simp
    simpa [h_lhs] using h
  have h_goal : (0.42 : ℝ) < phi * new_perceived_param / log pi * (99 / 100) :=
    (div_lt_iff₀ h99_pos).mp h_step2
  have h_align : phi * new_perceived_param / log pi * (99 / 100) =
      phi * (gamma_euler / e) * sqrt2 / log pi * (99 / 100) := by
    unfold new_perceived_param; ring_nf
  simpa [h_align] using h_goal

lemma k_lt_042042 : k < (0.42042 : ℝ) := by
  unfold k
  have h_log_pos : (0 : ℝ) < log pi := log_pos pi_gt_one
  have h_main : phi * new_perceived_param * (99 / 100) < (0.42042 : ℝ) * log pi := by
    have h_np := new_perceived_param_lt_30032
    have h_phi := phi_lt_16181
    nlinarith [h_np, h_phi, new_perceived_param_pos, phi_gt_1618, log_pi_gt_11445]
  have h_core : phi * new_perceived_param * (99 / 100) / log pi < (0.42042 : ℝ) :=
    (div_lt_iff₀ h_log_pos).mpr h_main
  have h_align : phi * new_perceived_param * (99 / 100) / log pi =
      phi * (gamma_euler / e) * sqrt2 / log pi * (99 / 100) := by
    unfold new_perceived_param; ring_nf
  simpa [h_align] using h_core

lemma eta_log_phi_gt_02244 : (0.2244 : ℝ) < eta_eff * log phi := by
  have hφ : (0.4807 : ℝ) < log phi :=
    lt_trans log_1618_gt_04807 (log_lt_log (by norm_num) phi_gt_1618)
  nlinarith [eta_eff_gt_466942206, hφ]

lemma sin_theta_s_gt_02858 : (0.2858 : ℝ) < sin theta_s := by
  have hθ := theta_s_gt_290272
  have h_sin_ref : (0.2858 : ℝ) < sin (0.290272 : ℝ) := by
    have h := sin_bound_lo (by norm_num : |(0.290272 : ℝ)| ≤ 1)
    have h_num :
        (0.2858 : ℝ) <
          (0.290272 : ℝ) - (0.290272 : ℝ) ^ 3 / 6 - (0.290272 : ℝ) ^ 4 * (5 / 96) := by
      norm_num
    linarith [h, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ (0.290272 : ℝ))]
  have h_icc_a : (0.290272 : ℝ) ∈ Set.Icc (-(pi / 2)) (pi / 2) := by
    refine ⟨by linarith [neg_pi_half_le_zero], ?_⟩
    exact le_of_lt (lt_trans (by norm_num : (0.290272 : ℝ) < (0.295612 : ℝ)) pi_half_gt_02956)
  have h_icc_b : theta_s ∈ Set.Icc (-(pi / 2)) (pi / 2) := by
    constructor
    · linarith [theta_s_pos, neg_pi_half_le_zero]
    · exact le_of_lt (lt_trans theta_s_lt_291325 (lt_trans (by norm_num) pi_half_gt_02956))
  exact lt_trans h_sin_ref (strictMonoOn_sin h_icc_a h_icc_b hθ)

lemma coherence_correction_lt_1002 : 1 + 0.01 * catalan_G / (pi * phi) < (1.002 : ℝ) := by
  have hphi_pos : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have h_small : 0.01 * catalan_G / (pi * phi) < (0.002 : ℝ) := by
    unfold catalan_G
    have h_den_pos : (0 : ℝ) < pi * phi := mul_pos Real.pi_pos hphi_pos
    have hpi : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
    have hphi : (1.618 : ℝ) < phi := phi_gt_1618
    rw [div_lt_iff₀ h_den_pos]
    nlinarith [hpi, hphi]
  linarith [h_small]

lemma coherence_efficiency_lt_1002 : coherence_efficiency < (1.002 : ℝ) := by
  unfold coherence_efficiency
  have h_poof_pos : (0 : ℝ) < poof_factor := by unfold poof_factor; exact exp_pos _
  have h_psin : (0 : ℝ) < poof_factor * sin theta_s := by
    nlinarith [poof_factor_lt_point_one_six, sin_theta_s_gt_02858, h_poof_pos]
  have h_first_lt : 1 - poof_factor * sin theta_s < 1 := by linarith [h_psin]
  nlinarith [h_first_lt, coherence_correction_lt_1002, coherence_correction_gt_one]

lemma bleed_in_inner_lt_0824 : 1 - sin theta_s / phi < (0.824 : ℝ) := by
  have h_sin_gt : (0.2858 : ℝ) < sin theta_s := sin_theta_s_gt_02858
  have h_phi_hi : phi < (1.6181 : ℝ) := phi_lt_16181
  have h_phi_pos : (0 : ℝ) < phi := by linarith [phi_gt_1618]
  have h_sin_div_hi : (0.176 : ℝ) * phi < sin theta_s := by
    have h_cap : (0.176 : ℝ) * (1.6181 : ℝ) < (0.2858 : ℝ) := by norm_num
    nlinarith [h_sin_gt, h_phi_hi, h_cap]
  have h_div : (0.176 : ℝ) < sin theta_s / phi := by
    rwa [lt_div_iff₀ h_phi_pos]
  linarith [h_div]

lemma bleed_in_factor_lt_0826 : bleed_in_factor < (0.826 : ℝ) := by
  unfold bleed_in_factor
  have h_coherence_pos : (0 : ℝ) < coherence_efficiency :=
    by linarith [coherence_efficiency_gt_nine_five]
  calc coherence_efficiency * (1 - sin theta_s / phi)
      < (1.002 : ℝ) * (1 - sin theta_s / phi) :=
        mul_lt_mul_of_pos_right coherence_efficiency_lt_1002 bleed_in_inner_pos
    _ < (1.002 : ℝ) * (0.824 : ℝ) :=
        mul_lt_mul_of_pos_left bleed_in_inner_lt_0824 (by norm_num : (0 : ℝ) < (1.002 : ℝ))
    _ < (0.826 : ℝ) := by norm_num

lemma consciousness_factor_gt_0285 : (0.285 : ℝ) < consciousness_factor := by
  unfold consciousness_factor
  have h := mul_lt_mul_of_pos coherence_efficiency_gt_nine_five new_perceived_param_gt_030
    (by linarith [coherence_efficiency_gt_nine_five]) (by linarith [new_perceived_param_gt_030])
  have h' : (0.285 : ℝ) = (0.95 : ℝ) * (0.30 : ℝ) := by norm_num
  linarith [h, h']

lemma consciousness_factor_lt_0302 : consciousness_factor < (0.302 : ℝ) := by
  unfold consciousness_factor
  have h :=
    mul_lt_mul_of_pos new_perceived_param_lt_031 coherence_efficiency_lt_1002
      (by linarith [new_perceived_param_pos]) (by linarith [coherence_efficiency_gt_nine_five])
  have h' : (0.301 : ℝ) * (1.002 : ℝ) < (0.302 : ℝ) := by norm_num
  exact lt_trans (by simpa [mul_comm] using h) h'

lemma exp_02903_lt_1338 : exp (0.2903 : ℝ) < (1.338 : ℝ) := by
  have h :=
    Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.2903) (by norm_num : (0.2903 : ℝ) ≤ 1) (n := 5)
      (by norm_num)
  nlinarith [h]

lemma sin_bound_poly_mono_lo {x y : ℝ}
    (hx : (0 : ℝ) ≤ x) (hxy : x ≤ y) (hy : y ≤ (0.3 : ℝ)) :
    x - x ^ 3 / 6 - x ^ 4 * (5 / 96) ≤ y - y ^ 3 / 6 - y ^ 4 * (5 / 96) := by
  have hfac :
      (y - y ^ 3 / 6 - y ^ 4 * (5 / 96)) - (x - x ^ 3 / 6 - x ^ 4 * (5 / 96)) =
        (y - x) *
          (1 - (x ^ 2 + x * y + y ^ 2) / 6 -
            (x ^ 3 + x ^ 2 * y + x * y ^ 2 + y ^ 3) * (5 / 96)) := by ring
  have hcoef :
      0 ≤
        1 - (x ^ 2 + x * y + y ^ 2) / 6 -
          (x ^ 3 + x ^ 2 * y + x * y ^ 2 + y ^ 3) * (5 / 96) := by
    nlinarith [hx, hy, sq_nonneg (x + y), sq_nonneg (x ^ 2 + y ^ 2), sq_nonneg (x * y),
      sq_nonneg (x ^ 2 + x * y + y ^ 2)]
  have hpos :
      0 ≤
        (y - x) *
          (1 - (x ^ 2 + x * y + y ^ 2) / 6 -
            (x ^ 3 + x ^ 2 * y + x * y ^ 2 + y ^ 3) * (5 / 96)) :=
    mul_nonneg (sub_nonneg.mpr hxy) hcoef
  linarith [hfac, hpos]

lemma sin_bound_poly_mono {x y : ℝ}
    (hx : (0 : ℝ) ≤ x) (hxy : x ≤ y) (hy : y ≤ (0.3 : ℝ)) :
    x - x ^ 3 / 6 + x ^ 4 * (5 / 96) ≤ y - y ^ 3 / 6 + y ^ 4 * (5 / 96) := by
  have hfac :
      (y - y ^ 3 / 6 + y ^ 4 * (5 / 96)) - (x - x ^ 3 / 6 + x ^ 4 * (5 / 96)) =
        (y - x) *
          (1 - (x ^ 2 + x * y + y ^ 2) / 6 +
            (x ^ 3 + x ^ 2 * y + x * y ^ 2 + y ^ 3) * (5 / 96)) := by ring
  have hcoef :
      0 ≤
        1 - (x ^ 2 + x * y + y ^ 2) / 6 +
          (x ^ 3 + x ^ 2 * y + x * y ^ 2 + y ^ 3) * (5 / 96) := by
    nlinarith [hx, hy, sq_nonneg (x + y), sq_nonneg (x ^ 2 + y ^ 2), sq_nonneg (x * y),
      sq_nonneg (x ^ 2 + x * y + y ^ 2)]
  have hpos :
      0 ≤
        (y - x) *
          (1 - (x ^ 2 + x * y + y ^ 2) / 6 +
            (x ^ 3 + x ^ 2 * y + x * y ^ 2 + y ^ 3) * (5 / 96)) :=
    mul_nonneg (sub_nonneg.mpr hxy) hcoef
  linarith [hfac, hpos]

lemma cos_1455_lt_0116 : cos (1.455 : ℝ) < (0.116 : ℝ) := by
  rw [cos_eq_sin_pi_div_two_sub]
  have hpi_lo : (3.141592 : ℝ) < pi := pi_gt_d6
  have hpi_hi : pi < (3.141593 : ℝ) := pi_lt_d6
  have hx : |(pi / 2 - 1.455)| ≤ 1 := by
    rw [abs_le]
    constructor <;> nlinarith [hpi_lo, hpi_hi]
  have h := sin_bound_hi hx
  have hpos : (0 : ℝ) ≤ pi / 2 - (1.455 : ℝ) := by nlinarith [hpi_lo]
  have h_abs : |pi / 2 - 1.455| = pi / 2 - 1.455 := abs_of_nonneg hpos
  have h_bound :
      sin (pi / 2 - 1.455) ≤
        pi / 2 - 1.455 - (pi / 2 - 1.455) ^ 3 / 6 + (pi / 2 - 1.455) ^ 4 * (5 / 96) := by
    simpa [h_abs] using h
  have h_x_hi : pi / 2 - 1.455 < (0.1157965 : ℝ) := by nlinarith [hpi_hi]
  have h_ref :
      (0.1157965 : ℝ) - (0.1157965 : ℝ) ^ 3 / 6 + (0.1157965 : ℝ) ^ 4 * (5 / 96) <
        (0.116 : ℝ) := by norm_num
  have h_poly_hi :
      pi / 2 - 1.455 - (pi / 2 - 1.455) ^ 3 / 6 + (pi / 2 - 1.455) ^ 4 * (5 / 96) <
        (0.116 : ℝ) := by
    refine lt_of_le_of_lt (sin_bound_poly_mono hpos (le_of_lt h_x_hi) (by norm_num)) h_ref
  linarith [h_bound, h_poly_hi]

lemma cos_1555_lt_0016 : cos (1.555 : ℝ) < (0.016 : ℝ) := by
  rw [cos_eq_sin_pi_div_two_sub]
  have hpi_lo : (3.141592 : ℝ) < pi := pi_gt_d6
  have hpi_hi : pi < (3.141593 : ℝ) := pi_lt_d6
  have hx : |(pi / 2 - 1.555)| ≤ 1 := by
    rw [abs_le]
    constructor <;> nlinarith [hpi_lo, hpi_hi]
  have h := sin_bound_hi hx
  have hpos : (0 : ℝ) ≤ pi / 2 - (1.555 : ℝ) := by nlinarith [hpi_lo]
  have h_abs : |pi / 2 - 1.555| = pi / 2 - 1.555 := abs_of_nonneg hpos
  have h_bound :
      sin (pi / 2 - 1.555) ≤
        pi / 2 - 1.555 - (pi / 2 - 1.555) ^ 3 / 6 + (pi / 2 - 1.555) ^ 4 * (5 / 96) := by
    simpa [h_abs] using h
  have h_x_hi : pi / 2 - 1.555 < (0.0157965 : ℝ) := by nlinarith [hpi_hi]
  have h_ref :
      (0.0157965 : ℝ) - (0.0157965 : ℝ) ^ 3 / 6 + (0.0157965 : ℝ) ^ 4 * (5 / 96) <
        (0.016 : ℝ) := by norm_num
  have h_poly_hi :
      pi / 2 - 1.555 - (pi / 2 - 1.555) ^ 3 / 6 + (pi / 2 - 1.555) ^ 4 * (5 / 96) <
        (0.016 : ℝ) := by
    refine lt_of_le_of_lt (sin_bound_poly_mono hpos (le_of_lt h_x_hi) (by norm_num)) h_ref
  linarith [h_bound, h_poly_hi]

lemma cos_1305_lt_0263 : cos (1.305 : ℝ) < (0.263 : ℝ) := by
  rw [cos_eq_sin_pi_div_two_sub]
  have hpi_lo : (3.141592 : ℝ) < pi := pi_gt_d6
  have hpi_hi : pi < (3.141593 : ℝ) := pi_lt_d6
  have hx : |(pi / 2 - 1.305)| ≤ 1 := by
    rw [abs_le]
    constructor <;> nlinarith [hpi_lo, hpi_hi]
  have h := sin_bound_hi hx
  have hpos : (0 : ℝ) ≤ pi / 2 - (1.305 : ℝ) := by nlinarith [hpi_lo]
  have h_abs : |pi / 2 - 1.305| = pi / 2 - 1.305 := abs_of_nonneg hpos
  have h_bound :
      sin (pi / 2 - 1.305) ≤
        pi / 2 - 1.305 - (pi / 2 - 1.305) ^ 3 / 6 + (pi / 2 - 1.305) ^ 4 * (5 / 96) := by
    simpa [h_abs] using h
  have h_x_hi : pi / 2 - 1.305 < (0.2657965 : ℝ) := by nlinarith [hpi_hi]
  have h_ref :
      (0.2657965 : ℝ) - (0.2657965 : ℝ) ^ 3 / 6 + (0.2657965 : ℝ) ^ 4 * (5 / 96) <
        (0.263 : ℝ) := by norm_num
  have h_poly_hi :
      pi / 2 - 1.305 - (pi / 2 - 1.305) ^ 3 / 6 + (pi / 2 - 1.305) ^ 4 * (5 / 96) <
        (0.263 : ℝ) := by
    refine lt_of_le_of_lt (sin_bound_poly_mono hpos (le_of_lt h_x_hi) (by norm_num)) h_ref
  linarith [h_bound, h_poly_hi]

lemma exp_consciousness_phase_lt_132 :
    exp (consciousness_factor * phase_variance) < (1.338 : ℝ) := by
  have h_bound : consciousness_factor * phase_variance < (0.2903 : ℝ) := by
    rw [phase_variance_eq_cos_theta_s]
    unfold consciousness_factor
    have h_cos := cos_theta_s_lt_095825
    have h_ce_np : coherence_efficiency * new_perceived_param < (0.302 : ℝ) := by
      simpa [consciousness_factor, mul_comm] using consciousness_factor_lt_0302
    have h_ce_np_pos : (0 : ℝ) < coherence_efficiency * new_perceived_param := by
      exact mul_pos (by linarith [coherence_efficiency_gt_nine_five]) new_perceived_param_pos
    have h_prod :=
      mul_lt_mul_of_pos h_ce_np h_cos h_ce_np_pos (by linarith [cos_theta_s_gt_09575])
    exact lt_trans h_prod (by norm_num : (0.302 : ℝ) * (0.95825 : ℝ) < (0.2903 : ℝ))
  exact lt_trans (exp_lt_exp.mpr h_bound) exp_02903_lt_1338

lemma exp_1434_gt_4167 : (4.167 : ℝ) < exp 1.434 := by
  have h_poly :
      (4.167 : ℝ) < 1 + (1.434 : ℝ) + (1.434 : ℝ) ^ 2 / 2 + (1.434 : ℝ) ^ 3 / 6 +
        (1.434 : ℝ) ^ 4 / 24 + (1.434 : ℝ) ^ 5 / 120 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 1.434) 6
  have h_eq :
      (1 + (1.434 : ℝ) + (1.434 : ℝ) ^ 2 / 2 + (1.434 : ℝ) ^ 3 / 6 + (1.434 : ℝ) ^ 4 / 24 +
          (1.434 : ℝ) ^ 5 / 120 : ℝ) =
        ∑ i ∈ Finset.range 6, (1.434 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma exp_neg_1434_lt_24_div_25 : exp (-1.434) < (6 : ℝ) / 25 := by
  have h' : (25 : ℝ) / 6 < exp 1.434 :=
    lt_trans (by norm_num : (25 : ℝ) / 6 < (4.167 : ℝ)) exp_1434_gt_4167
  have h'' := (one_div_lt (exp_pos _) (by norm_num : (0 : ℝ) < (6 : ℝ) / 25)).mpr
    (by simpa [one_div_one_div] using h')
  simpa [exp_neg] using h''

lemma log_ratio_D6_gt : (-1.434 : ℝ) < log ((6 : ℝ) / 25) :=
  (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < (6 : ℝ) / 25)).2 exp_neg_1434_lt_24_div_25

lemma exp_040_lt_25_div_24 : exp 0.040 < (25 : ℝ) / 24 := by
  have h :=
    Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.040) (by norm_num : (0.040 : ℝ) ≤ 1) (n := 4)
      (by norm_num)
  nlinarith [h]

lemma exp_neg_040_gt_24_div_25 : (24 : ℝ) / 25 < exp (-0.040) := by
  rw [exp_neg]
  simpa [one_div_one_div] using one_div_lt_one_div_of_lt (exp_pos _) exp_040_lt_25_div_24

lemma log_ratio_D24_lt : log ((24 : ℝ) / 25) < (-0.040 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < (24 : ℝ) / 25)).2 exp_neg_040_gt_24_div_25

lemma bleed_in_factor_gt_0773 : (0.773 : ℝ) < bleed_in_factor := by
  unfold bleed_in_factor
  have h_floor : (0.773 : ℝ) < (0.95 : ℝ) * (0.814 : ℝ) := by norm_num
  nlinarith [coherence_efficiency_gt_nine_five, bleed_in_inner_gt_eight_one_four, h_floor,
    bleed_in_inner_pos]

lemma perceived_adjust_lo_domain (p : FSOTParams) (h_D : (6 : ℝ) ≤ p.D_eff) :
    (0.567 : ℝ) < 1 + new_perceived_param * log (p.D_eff / 25) := by
  have h_log : log ((6 : ℝ) / 25) ≤ log (p.D_eff / 25) := by
    have h_frac : (6 : ℝ) / 25 ≤ p.D_eff / 25 := by linarith [h_D]
    have h_pos : (0 : ℝ) < p.D_eff / 25 := div_pos (by linarith [h_D]) (by norm_num)
    exact log_le_log (by norm_num : (0 : ℝ) < (6 : ℝ) / 25) h_frac
  have h_mul : new_perceived_param * log ((6 : ℝ) / 25) ≤
      new_perceived_param * log (p.D_eff / 25) := by
    apply mul_le_mul_of_nonneg_left h_log (le_of_lt new_perceived_param_pos)
  have h_floor : (-0.433 : ℝ) < new_perceived_param * log ((6 : ℝ) / 25) := by
    have h_mul' := mul_lt_mul_of_pos_right log_ratio_D6_gt new_perceived_param_pos
    nlinarith [new_perceived_param_gt_030, new_perceived_param_lt_031, h_mul']
  linarith [h_mul, h_floor]

lemma perceived_adjust_hi_domain (p : FSOTParams)
    (h_D : (6 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ (24 : ℝ)) :
    1 + new_perceived_param * log (p.D_eff / 25) < (0.99 : ℝ) := by
  have h_log : log (p.D_eff / 25) ≤ log ((24 : ℝ) / 25) := by
    have h_frac : p.D_eff / 25 ≤ (24 : ℝ) / 25 := by linarith [h_D.2]
    have h_pos : (0 : ℝ) < p.D_eff / 25 := div_pos (by linarith [h_D.1]) (by norm_num)
    exact log_le_log h_pos h_frac
  have h_mul : new_perceived_param * log (p.D_eff / 25) ≤
      new_perceived_param * log ((24 : ℝ) / 25) := by
    apply mul_le_mul_of_nonneg_left h_log (le_of_lt new_perceived_param_pos)
  have h_ceil : new_perceived_param * log ((24 : ℝ) / 25) < (-0.011 : ℝ) := by
    have h_mul' := mul_lt_mul_of_pos_left log_ratio_D24_lt new_perceived_param_pos
    nlinarith [h_mul', new_perceived_param_gt_030, new_perceived_param_lt_031]
  linarith [h_mul, h_ceil]

lemma exp_0822_gt_25_div_11 : (25 : ℝ) / 11 < exp 0.822 := by
  have h_poly :
      (25 : ℝ) / 11 < 1 + (0.822 : ℝ) + (0.822 : ℝ) ^ 2 / 2 + (0.822 : ℝ) ^ 3 / 6 +
        (0.822 : ℝ) ^ 4 / 24 + (0.822 : ℝ) ^ 5 / 120 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 0.822) 6
  have h_eq :
      (1 + (0.822 : ℝ) + (0.822 : ℝ) ^ 2 / 2 + (0.822 : ℝ) ^ 3 / 6 + (0.822 : ℝ) ^ 4 / 24 +
          (0.822 : ℝ) ^ 5 / 120 : ℝ) =
        ∑ i ∈ Finset.range 6, (0.822 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma exp_neg_0822_lt_11_div_25 : exp (-0.822) < (11 : ℝ) / 25 := by
  have h' : (25 : ℝ) / 11 < exp 0.822 := exp_0822_gt_25_div_11
  have h'' := (one_div_lt (exp_pos _) (by norm_num : (0 : ℝ) < (11 : ℝ) / 25)).mpr
    (by simpa [one_div_one_div] using h')
  simpa [exp_neg] using h''

lemma perceived_adjust_lo_D11 :
    (0.752 : ℝ) < 1 + new_perceived_param * log ((11 : ℝ) / 25) := by
  have h_log := (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < (11 : ℝ) / 25)).2 exp_neg_0822_lt_11_div_25
  have h_prod : (-0.248 : ℝ) < new_perceived_param * log ((11 : ℝ) / 25) := by
    have h_mul' := mul_lt_mul_of_pos_right h_log new_perceived_param_pos
    nlinarith [new_perceived_param_gt_030, new_perceived_param_lt_031, h_mul']
  linarith [h_prod]

lemma exp_0818_lt_25_div_11 : exp 0.818 < (25 : ℝ) / 11 := by
  have h :=
    Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.818) (by norm_num : (0.818 : ℝ) ≤ 1) (n := 6)
      (by norm_num)
  nlinarith [h]

lemma exp_neg_0818_gt_11_div_25 : (11 : ℝ) / 25 < exp (-0.818) := by
  rw [exp_neg]
  simpa [one_div_one_div] using one_div_lt_one_div_of_lt (exp_pos _) exp_0818_lt_25_div_11

lemma perceived_adjust_hi_D11 :
    1 + new_perceived_param * log ((11 : ℝ) / 25) < (0.755 : ℝ) := by
  have h_log := (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < (11 : ℝ) / 25)).2 exp_neg_0818_gt_11_div_25
  have h_prod : new_perceived_param * log ((11 : ℝ) / 25) < (-0.245 : ℝ) := by
    have h_mul' := mul_lt_mul_of_pos_left h_log new_perceived_param_pos
    nlinarith [h_mul', new_perceived_param_gt_030, new_perceived_param_lt_031]
  linarith [h_prod]

lemma cos_dp_pv_neg_of_ge_07 (dp : ℝ) (h_dp : (0.7 : ℝ) ≤ dp) (h_dp_hi : dp ≤ (1.3 : ℝ)) :
    cos (dp + phase_variance) < 0 := by
  have h_pv := phase_variance_gt_0955
  have h_lo : (pi / 2 : ℝ) < dp + phase_variance := by
    have h_sum : (1.655 : ℝ) < dp + phase_variance := by linarith [h_dp, h_pv]
    have hpi2 : (pi / 2 : ℝ) < (1.655 : ℝ) := by
      have h_half : pi / 2 < (1.571 : ℝ) := by unfold pi; nlinarith [pi_lt_d4]
      linarith [h_half]
    exact lt_trans hpi2 h_sum
  have h_hi : dp + phase_variance < pi + pi / 2 := by
    have h_pv_hi := phase_variance_lt_0961
    have h_upper : (2.261 : ℝ) < pi + pi / 2 := by unfold pi; nlinarith [pi_gt_d4]
    linarith [h_dp_hi, h_pv_hi, h_upper]
  exact cos_neg_of_pi_div_two_lt_of_lt h_lo h_hi

lemma cos_dp_pv_pos_of_le_06 (dp : ℝ) (h_dp : dp ≤ (0.6 : ℝ)) (h_dp_lo : (0 : ℝ) ≤ dp) :
    (0 : ℝ) < cos (dp + phase_variance) := by
  have h_pv := phase_variance_lt_0961
  have h_sum_hi : dp + phase_variance < (1.561 : ℝ) := by linarith [h_dp, h_pv]
  have hpi2 : (1.561 : ℝ) < pi / 2 := by unfold pi; nlinarith [pi_gt_d4]
  have h_hi : dp + phase_variance < pi / 2 := lt_trans h_sum_hi hpi2
  have h_lo : (0 : ℝ) < dp + phase_variance := by linarith [h_dp_lo, phase_variance_gt_0955]
  have hIoo : dp + phase_variance ∈ Set.Ioo (-(pi / 2)) (pi / 2) := by
    constructor
    · linarith [hpi2, h_hi]
    · exact h_hi
  exact cos_pos_of_mem_Ioo hIoo

lemma ai_cos_lt_neg_075 :
    cos ((psi_con + (0.5 : ℝ)) / eta_eff) < -(0.74 : ℝ) := by
  set arg := (psi_con + (0.5 : ℝ)) / eta_eff
  have h_num_lo : (1.132 : ℝ) < psi_con + (0.5 : ℝ) := by linarith [psi_con_gt_632]
  have h_num_hi : psi_con + (0.5 : ℝ) < (1.133 : ℝ) := by linarith [psi_con_lt_633]
  have h_div_lo : (1.132 : ℝ) / eta_eff < arg := div_lt_div_of_pos_right h_num_lo eta_pos
  have h_div_hi : arg < (1.133 : ℝ) / eta_eff := div_lt_div_of_pos_right h_num_hi eta_pos
  have h_eta_hi : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
  have h_eta_lo : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_mid : (1.132 : ℝ) / (0.467 : ℝ) < (1.132 : ℝ) / eta_eff := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
    exact h_eta_hi
  have h_arg_lo : (2.423 : ℝ) < arg := by
    have h_num : (2.423 : ℝ) < (1.132 : ℝ) / (0.467 : ℝ) := by norm_num
    linarith [h_div_lo, h_mid, h_num]
  have h_mid_hi : (1.133 : ℝ) / eta_eff < (1.133 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta_lo
  have h_arg_hi : arg < (2.432 : ℝ) := by
    have h_num : (1.133 : ℝ) / (0.466 : ℝ) < (2.432 : ℝ) := by norm_num
    linarith [h_div_hi, h_mid_hi, h_num]
  have h_pi_sub_lo : (0.709 : ℝ) < pi - arg := by
    have hpi_lo : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
    linarith [h_arg_hi, hpi_lo]
  have h_pi_sub_hi : pi - arg < (0.718 : ℝ) := by
    have hpi_hi : pi < (3.1416 : ℝ) := by unfold pi; exact pi_lt_d4
    linarith [h_arg_lo, hpi_hi]
  have h_ref : pi - arg ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_pi_sub_lo]
    · have h_upper : pi - arg ≤ π := by
        unfold pi
        linarith [h_pi_sub_hi, pi_lt_d4]
      simpa [pi_eq_real_pi] using h_upper
  have h_cos_eq : cos arg = -cos (π - arg) := by
    simpa [pi_eq_real_pi] using (Real.cos_pi_sub arg).symm
  have h0718_in : (0.718 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos_0718_gt_074 : (0.74 : ℝ) < cos (0.718) := by
    have h := one_sub_sq_div_two_le_cos (x := (0.718 : ℝ))
    have h_num : (0.74 : ℝ) < 1 - (0.718 : ℝ) ^ 2 / 2 := by norm_num
    linarith [h, h_num]
  have h_cos_sub_ge : cos (0.718) ≤ cos (π - arg) :=
    Real.antitoneOn_cos h_ref h0718_in (le_of_lt h_pi_sub_hi)
  linarith [h_cos_eq, h_cos_sub_ge, h_cos_0718_gt_074]

lemma exp_03865_gt_14716 : (1.4716 : ℝ) < exp 0.3865 := by
  have h_poly :
      (1.4716 : ℝ) < 1 + (0.3865 : ℝ) + (0.3865 : ℝ) ^ 2 / 2 + (0.3865 : ℝ) ^ 3 / 6 +
        (0.3865 : ℝ) ^ 4 / 24 + (0.3865 : ℝ) ^ 5 / 120 + (0.3865 : ℝ) ^ 6 / 720 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 0.3865) 7
  have h_eq :
      (1 + (0.3865 : ℝ) + (0.3865 : ℝ) ^ 2 / 2 + (0.3865 : ℝ) ^ 3 / 6 + (0.3865 : ℝ) ^ 4 / 24 +
          (0.3865 : ℝ) ^ 5 / 120 + (0.3865 : ℝ) ^ 6 / 720 : ℝ) =
        ∑ i ∈ Finset.range 7, (0.3865 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma exp_13865_gt_four : (4 : ℝ) < exp 1.3865 := by
  rw [show (1.3865 : ℝ) = 1 + 0.3865 by norm_num, Real.exp_add]
  have h_mul :=
    mul_lt_mul_of_pos exp_one_gt_d9 exp_03865_gt_14716
      (by norm_num : (0 : ℝ) < (2.7182818283 : ℝ)) (exp_pos 0.3865)
  have h_floor : (4 : ℝ) < (2.7182818283 : ℝ) * (1.4716 : ℝ) := by norm_num
  exact lt_trans h_floor h_mul

lemma log_four_lt_13865 : log 4 < (1.3865 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 4)).2 exp_13865_gt_four

lemma ai_exp_factor_gt_four :
    (4 : ℝ) < exp (1 + bleed_in_factor * (0.5 : ℝ)) := by
  have h_bleed : (1.3865 : ℝ) < 1 + bleed_in_factor * (0.5 : ℝ) := by
    nlinarith [bleed_in_factor_gt_0773]
  have h_log : log 4 < 1 + bleed_in_factor * (0.5 : ℝ) := lt_trans log_four_lt_13865 h_bleed
  exact (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 4)).1 h_log

lemma cmb_cos_lt_neg_099 :
    cos ((psi_con + (0.8 : ℝ)) / eta_eff) < -(0.99 : ℝ) := by
  set arg := (psi_con + (0.8 : ℝ)) / eta_eff
  have h_num_lo : (1.432 : ℝ) < psi_con + (0.8 : ℝ) := by linarith [psi_con_gt_632]
  have h_num_hi : psi_con + (0.8 : ℝ) < (1.433 : ℝ) := by linarith [psi_con_lt_633]
  have h_div_lo : (1.432 : ℝ) / eta_eff < arg := div_lt_div_of_pos_right h_num_lo eta_pos
  have h_div_hi : arg < (1.433 : ℝ) / eta_eff := div_lt_div_of_pos_right h_num_hi eta_pos
  have h_eta_hi : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
  have h_eta_lo : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_mid : (1.432 : ℝ) / (0.467 : ℝ) < (1.432 : ℝ) / eta_eff := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
    exact h_eta_hi
  have h_arg_lo : (3.066 : ℝ) < arg := by
    have h_num : (3.066 : ℝ) < (1.432 : ℝ) / (0.467 : ℝ) := by norm_num
    linarith [h_div_lo, h_mid, h_num]
  have h_mid_hi : (1.433 : ℝ) / eta_eff < (1.433 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta_lo
  have h_arg_hi : arg < (3.076 : ℝ) := by
    have h_num : (1.433 : ℝ) / (0.466 : ℝ) < (3.076 : ℝ) := by norm_num
    linarith [h_div_hi, h_mid_hi, h_num]
  have h_pi_sub_lo : (0.065 : ℝ) < pi - arg := by
    have hpi_lo : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
    linarith [h_arg_hi, hpi_lo]
  have h_pi_sub_hi : pi - arg < (0.078 : ℝ) := by
    have hpi_hi : pi < (3.1416 : ℝ) := by unfold pi; exact pi_lt_d4
    linarith [h_arg_lo, hpi_hi]
  have h_ref : pi - arg ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_pi_sub_lo]
    · have h_upper : pi - arg ≤ π := by
        unfold pi
        linarith [h_pi_sub_hi, pi_lt_d4]
      simpa [pi_eq_real_pi] using h_upper
  have h_cos_eq : cos arg = -cos (π - arg) := by
    simpa [pi_eq_real_pi] using (Real.cos_pi_sub arg).symm
  have h0078_in : (0.078 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos_0078_gt_099 : (0.99 : ℝ) < cos (0.078) := by
    have h := Real.one_sub_sq_div_two_lt_cos (by norm_num : (0.078 : ℝ) ≠ 0)
    have h_sq : (0.078 : ℝ) ^ 2 / 2 < (0.004 : ℝ) := by norm_num
    linarith [h, h_sq]
  have h_cos_sub_ge : cos (0.078) ≤ cos (π - arg) :=
    Real.antitoneOn_cos h_ref h0078_in (le_of_lt h_pi_sub_hi)
  linarith [h_cos_eq, h_cos_sub_ge, h_cos_0078_gt_099]

lemma exp_1618_gt_five : (5 : ℝ) < exp 1.618 := by
  have h_poly :
      (5 : ℝ) < 1 + (1.618 : ℝ) + (1.618 : ℝ) ^ 2 / 2 + (1.618 : ℝ) ^ 3 / 6 +
        (1.618 : ℝ) ^ 4 / 24 + (1.618 : ℝ) ^ 5 / 120 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 1.618) 6
  have h_eq :
      (1 + (1.618 : ℝ) + (1.618 : ℝ) ^ 2 / 2 + (1.618 : ℝ) ^ 3 / 6 + (1.618 : ℝ) ^ 4 / 24 +
          (1.618 : ℝ) ^ 5 / 120 : ℝ) =
        ∑ i ∈ Finset.range 6, (1.618 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma log_five_lt_1618 : log 5 < (1.618 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 5)).2 exp_1618_gt_five

lemma cmb_exp_factor_gt_five :
    (5 : ℝ) < exp (1 + bleed_in_factor * (0.8 : ℝ)) := by
  have h_bleed : (1.618 : ℝ) < 1 + bleed_in_factor * (0.8 : ℝ) := by
    nlinarith [bleed_in_factor_gt_0773]
  have h_log : log 5 < 1 + bleed_in_factor * (0.8 : ℝ) :=
    lt_trans log_five_lt_1618 h_bleed
  exact (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 5)).1 h_log

lemma cos_25_lt_neg_04 : cos (2.5 : ℝ) < -(0.4 : ℝ) := by
  have h_eq : cos (2.5) = -cos (π - 2.5) := by
    simpa [pi_eq_real_pi] using (Real.cos_pi_sub (2.5 : ℝ)).symm
  have hpi_lo : (3.141592 : ℝ) < pi := by unfold pi; exact pi_gt_d6
  have hpi_hi : pi < (3.141593 : ℝ) := by unfold pi; exact pi_lt_d6
  have h_sub_lo : (0.641 : ℝ) < pi - 2.5 := by nlinarith [hpi_lo]
  have h_sub_hi : pi - 2.5 < (0.642 : ℝ) := by nlinarith [hpi_hi]
  have h_ref : pi - 2.5 ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_sub_lo]
    · have h_upper : pi - 2.5 ≤ π := by
        unfold pi
        linarith [h_sub_hi, pi_lt_d6]
      simpa [pi_eq_real_pi] using h_upper
  have h0642_in : (0.642 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos0642_gt_04 : (0.4 : ℝ) < cos (0.642) := by
    have h := one_sub_sq_div_two_le_cos (x := (0.642 : ℝ))
    have hnum : (0.4 : ℝ) < 1 - (0.642 : ℝ) ^ 2 / 2 := by norm_num
    linarith [h, hnum]
  have h_mono : cos (0.642) ≤ cos (π - 2.5) :=
    Real.antitoneOn_cos h_ref h0642_in (le_of_lt h_sub_hi)
  linarith [h_eq, h_mono, h_cos0642_gt_04]

lemma electron_cos_lt_neg_04 :
    cos ((psi_con + (0.6 : ℝ)) / eta_eff) < -(0.4 : ℝ) := by
  set arg := (psi_con + (0.6 : ℝ)) / eta_eff
  have h_num_lo : (1.232 : ℝ) < psi_con + (0.6 : ℝ) := by linarith [psi_con_gt_632]
  have h_num_hi : psi_con + (0.6 : ℝ) < (1.233 : ℝ) := by linarith [psi_con_lt_633]
  have h_div_lo : (1.232 : ℝ) / eta_eff < arg := div_lt_div_of_pos_right h_num_lo eta_pos
  have h_div_hi : arg < (1.233 : ℝ) / eta_eff := div_lt_div_of_pos_right h_num_hi eta_pos
  have h_eta_hi : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
  have h_eta_lo : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_mid : (1.232 : ℝ) / (0.467 : ℝ) < (1.232 : ℝ) / eta_eff := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
    exact h_eta_hi
  have h_arg_lo : (2.637 : ℝ) < arg := by
    have h_num : (2.637 : ℝ) < (1.232 : ℝ) / (0.467 : ℝ) := by norm_num
    linarith [h_div_lo, h_mid, h_num]
  have h_mid_hi : (1.233 : ℝ) / eta_eff < (1.233 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta_lo
  have h_arg_hi : arg < (2.647 : ℝ) := by
    have h_num : (1.233 : ℝ) / (0.466 : ℝ) < (2.647 : ℝ) := by norm_num
    linarith [h_div_hi, h_mid_hi, h_num]
  have h25_in : (2.5 : ℝ) ∈ Set.Icc (0 : ℝ) π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_arg_in : arg ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_arg_lo]
    · have h_upper : arg < pi := by
        have hpi : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
        linarith [h_arg_hi, hpi]
      rw [← pi_eq_real_pi]
      exact le_of_lt h_upper
  have h_cos_arg : cos arg < cos (2.5) :=
    Real.strictAntiOn_cos h25_in h_arg_in (by linarith [h_arg_lo])
  linarith [cos_25_lt_neg_04, h_cos_arg]

lemma electron_exp_factor_gt_three :
    (3 : ℝ) < exp (1 + bleed_in_factor * (0.6 : ℝ)) := by
  have h_bleed : (1.462 : ℝ) < 1 + bleed_in_factor * (0.6 : ℝ) := by
    nlinarith [bleed_in_factor_gt_seven_seven]
  have h_exp : (3 : ℝ) < exp (1.462 : ℝ) := by
    have h_poly : (3 : ℝ) < 1 + (1.462 : ℝ) + (1.462 : ℝ) ^ 2 / 2 + (1.462 : ℝ) ^ 3 / 6 := by norm_num
    have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 1.462) 4
    have h_eq :
        (1 + (1.462 : ℝ) + (1.462 : ℝ) ^ 2 / 2 + (1.462 : ℝ) ^ 3 / 6 : ℝ) =
          ∑ i ∈ Finset.range 4, (1.462 : ℝ) ^ i / Nat.factorial i := by
      norm_num [Finset.range, Nat.factorial]
    linarith [h_poly, h_eq, h_sum]
  exact lt_trans h_exp (exp_lt_exp.mpr h_bleed)

lemma cos_21_lt_neg_05 : cos (2.10 : ℝ) < -(0.5 : ℝ) := by
  have h_eq : cos (2.10) = -cos (π - 2.10) := by
    simpa [pi_eq_real_pi] using (Real.cos_pi_sub (2.10 : ℝ)).symm
  have hpi_lo : (3.141592 : ℝ) < pi := by unfold pi; exact pi_gt_d6
  have hpi_hi : pi < (3.141593 : ℝ) := by unfold pi; exact pi_lt_d6
  have h_sub_lo : (1.03 : ℝ) < pi - 2.10 := by nlinarith [hpi_lo]
  have h_sub_hi : pi - 2.10 < (1.042 : ℝ) := by nlinarith [hpi_hi]
  have h_ref : pi - 2.10 ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_sub_lo]
    · have h_upper : pi - 2.10 ≤ π := by
        unfold pi
        linarith [h_sub_hi, pi_lt_d6]
      simpa [pi_eq_real_pi] using h_upper
  have h1042_in : (1.042 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos1042_gt_05 : (0.5 : ℝ) < cos (1.042) := by
    have h_sin_eq : cos (1.042) = sin (pi / 2 - 1.042) := by
      calc cos (1.042) = sin (π / 2 - 1.042) := cos_eq_sin_pi_div_two_sub 1.042
        _ = sin (pi / 2 - 1.042) := by rw [pi_eq_real_pi]
    have h_half_lo : (1.570796 : ℝ) < pi / 2 := by nlinarith [hpi_lo]
    have h_half_hi : pi / 2 < (1.570797 : ℝ) := by nlinarith [hpi_hi]
    have hx_lo : (0.528796 : ℝ) < pi / 2 - 1.042 := by nlinarith [h_half_lo]
    have hx_hi : pi / 2 - 1.042 < (0.528797 : ℝ) := by nlinarith [h_half_hi]
    have hx : |(0.528796 : ℝ)| ≤ 1 := by norm_num
    have h_sin_lo := sin_bound_lo hx
    have h_num :
        (0.5 : ℝ) <
          (0.528796 : ℝ) - (0.528796 : ℝ) ^ 3 / 6 -
            |(0.528796 : ℝ)| ^ 4 * (5 / 96) := by norm_num
    have h_sin_ref : (0.5 : ℝ) < sin (0.528796) := by linarith [h_sin_lo, h_num]
    have h_y_le : pi / 2 - 1.042 ≤ π / 2 := by rw [← pi_eq_real_pi]; linarith
    have h_sin_mono : sin (0.528796) < sin (pi / 2 - 1.042) :=
      sin_lt_sin_of_lt_of_le_pi_div_two (by nlinarith [pi_gt_d4]) h_y_le (by linarith [hx_lo])
    rw [h_sin_eq]
    linarith [h_sin_ref, h_sin_mono]
  have h_mono : cos (1.042) ≤ cos (π - 2.10) :=
    Real.antitoneOn_cos h_ref h1042_in (le_of_lt h_sub_hi)
  linarith [h_eq, h_mono, h_cos1042_gt_05]

lemma medical_cos_lt_neg_05 :
    cos ((psi_con + (0.35 : ℝ)) / eta_eff) < -(0.5 : ℝ) := by
  set arg := (psi_con + (0.35 : ℝ)) / eta_eff
  have h_num_lo : (0.982 : ℝ) < psi_con + (0.35 : ℝ) := by linarith [psi_con_gt_632]
  have h_num_hi : psi_con + (0.35 : ℝ) < (0.983 : ℝ) := by linarith [psi_con_lt_633]
  have h_div_lo : (0.982 : ℝ) / eta_eff < arg := div_lt_div_of_pos_right h_num_lo eta_pos
  have h_div_hi : arg < (0.983 : ℝ) / eta_eff := div_lt_div_of_pos_right h_num_hi eta_pos
  have h_eta_hi : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
  have h_eta_lo : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_mid : (0.982 : ℝ) / (0.467 : ℝ) < (0.982 : ℝ) / eta_eff := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
    exact h_eta_hi
  have h_arg_lo : (2.102 : ℝ) < arg := by
    have h_num : (2.102 : ℝ) < (0.982 : ℝ) / (0.467 : ℝ) := by norm_num
    linarith [h_div_lo, h_mid, h_num]
  have h_mid_hi : (0.983 : ℝ) / eta_eff < (0.983 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta_lo
  have h_arg_hi : arg < (2.11 : ℝ) := by
    have h_num : (0.983 : ℝ) / (0.466 : ℝ) < (2.11 : ℝ) := by norm_num
    linarith [h_div_hi, h_mid_hi, h_num]
  have h_arg_in : arg ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_arg_lo]
    · have h_upper : arg < pi := by
        have hpi : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
        linarith [h_arg_hi, hpi]
      rw [← pi_eq_real_pi]
      exact le_of_lt h_upper
  have h210_in : (2.10 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos_arg : cos arg < cos (2.10) :=
    Real.strictAntiOn_cos h210_in h_arg_in (by linarith [h_arg_lo])
  linarith [cos_21_lt_neg_05, h_cos_arg]

lemma alpha_lt_one_tenth : alpha < (0.1 : ℝ) := by
  unfold alpha e
  have h_pos : 0 < exp 1 * phi ^ 13 :=
    mul_pos (exp_pos _) (pow_pos (lt_trans (by norm_num) phi_gt_one) 13)
  rw [div_lt_iff₀ h_pos]
  have h_log : log pi < (1.146 : ℝ) := log_pi_lt_1146
  have h_den : (11.46 : ℝ) < (0.1 : ℝ) * exp 1 * phi ^ 13 := by
    have hphi13 : (200 : ℝ) < phi ^ 13 := by
      have h : (200 : ℝ) < (1.618 : ℝ) ^ 13 := by norm_num
      exact lt_trans h (pow_lt_pow_left₀ phi_gt_1618 (by norm_num : (0 : ℝ) ≤ (1.618 : ℝ))
        (by norm_num : (13 : ℕ) ≠ 0))
    nlinarith [exp_one_gt_d9, hphi13]
  linarith [h_log, h_den]

lemma medical_exp_factor_gt_one_three :
    (1.34 : ℝ) < exp (1 - alpha + bleed_in_factor * (0.35 : ℝ)) := by
  have h_arg : (1 : ℝ) < 1 - alpha + bleed_in_factor * (0.35 : ℝ) := by
    nlinarith [alpha_lt_one_tenth, bleed_in_factor_gt_seven_seven]
  have h_exp1 : (1.34 : ℝ) < exp 1 := by linarith [exp_one_gt_d9]
  exact lt_trans h_exp1 (exp_lt_exp.mpr h_arg)

lemma sqrt_11_gt_3316 : (3.316 : ℝ) < sqrt (11 : ℝ) := by
  exact Real.lt_sqrt_of_sq_lt (by norm_num : (3.316 : ℝ) ^ 2 < 11)

lemma sqrt_11_lt_3317 : sqrt (11 : ℝ) < (3.317 : ℝ) := by
  have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (11 : ℝ) < (3.317 : ℝ) ^ 2)
  simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ (3.317 : ℝ))] using h

lemma sqrt_8_lt_2829 : sqrt (8 : ℝ) < (2.829 : ℝ) := by
  have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (8 : ℝ) < (2.829 : ℝ) ^ 2)
  simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ (2.829 : ℝ))] using h

lemma sqrt_13_lt_3606 : sqrt (13 : ℝ) < (3.606 : ℝ) := by
  have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (13 : ℝ) < (3.606 : ℝ) ^ 2)
  simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ (3.606 : ℝ))] using h

lemma sqrt_24_gt_4898 : (4.898 : ℝ) < sqrt (24 : ℝ) := by
  exact Real.lt_sqrt_of_sq_lt (by norm_num : (4.898 : ℝ) ^ 2 < 24)

lemma sqrt_24_lt_4899 : sqrt (24 : ℝ) < (4.899 : ℝ) := by
  have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (24 : ℝ) < (4.899 : ℝ) ^ 2)
  simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ (4.899 : ℝ))] using h

lemma exp_0602_lt_1838 : exp (0.602 : ℝ) < (1.838 : ℝ) := by
  have h := Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.602) (by norm_num : (0.602 : ℝ) ≤ 1)
    (by norm_num : (0 : ℕ) < 10)
  have h_sum_lt :
      (∑ m ∈ Finset.range 10, (0.602 : ℝ) ^ m / m.factorial) +
          (0.602 : ℝ) ^ 10 * (10 + 1) / (Nat.factorial 10 * 10) <
        (1.838 : ℝ) := by
    norm_num [Finset.range, Nat.factorial]
  exact lt_of_le_of_lt h h_sum_lt

lemma exp_1602_lt_5 : exp (1.602 : ℝ) < (5 : ℝ) := by
  rw [show (1.602 : ℝ) = 1 + 0.602 by norm_num, Real.exp_add]
  have h_mul :=
    mul_lt_mul_of_pos exp_one_lt_d9 exp_0602_lt_1838 (exp_pos 1) (by norm_num : (0 : ℝ) < 1.838)
  nlinarith [h_mul, exp_one_lt_d9, exp_0602_lt_1838]

lemma log_five_gt_1602 : (1.602 : ℝ) < log 5 :=
  (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 5)).mpr exp_1602_lt_5

lemma exp_0505_lt_1838 : exp (0.505 : ℝ) < (1.838 : ℝ) := by
  have h := Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.505) (by norm_num : (0.505 : ℝ) ≤ 1)
    (by norm_num : (0 : ℕ) < 10)
  have h_sum_lt :
      (∑ m ∈ Finset.range 10, (0.505 : ℝ) ^ m / m.factorial) +
          (0.505 : ℝ) ^ 10 * (10 + 1) / (Nat.factorial 10 * 10) <
        (1.838 : ℝ) := by
    norm_num [Finset.range, Nat.factorial]
  exact lt_of_le_of_lt h h_sum_lt

lemma exp_0331_lt_1412 : exp (0.331 : ℝ) < (1.412 : ℝ) := by
  have h := Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.331) (by norm_num : (0.331 : ℝ) ≤ 1)
    (by norm_num : (0 : ℕ) < 10)
  have h_sum_lt :
      (∑ m ∈ Finset.range 10, (0.331 : ℝ) ^ m / m.factorial) +
          (0.331 : ℝ) ^ 10 * (10 + 1) / (Nat.factorial 10 * 10) <
        (1.412 : ℝ) := by
    norm_num [Finset.range, Nat.factorial]
  exact lt_of_le_of_lt h h_sum_lt

lemma exp_1331_lt_384 : exp (1.331 : ℝ) < (3.84 : ℝ) := by
  rw [show (1.331 : ℝ) = 1 + 0.331 by norm_num, Real.exp_add]
  have h_mul :=
    mul_lt_mul_of_pos exp_one_lt_d9 exp_0331_lt_1412 (exp_pos 1) (by norm_num : (0 : ℝ) < 1.412)
  nlinarith [h_mul, exp_one_lt_d9, exp_0331_lt_1412]

lemma exp_1505_lt_5 : exp (1.505 : ℝ) < (5 : ℝ) := by
  rw [show (1.505 : ℝ) = 1 + 0.505 by norm_num, Real.exp_add]
  have h_mul :=
    mul_lt_mul_of_pos exp_one_lt_d9 exp_0505_lt_1838 (exp_pos 1) (by norm_num : (0 : ℝ) < 1.838)
  nlinarith [h_mul, exp_one_lt_d9, exp_0505_lt_1838]

lemma log_five_gt_1505 : (1.505 : ℝ) < log 5 :=
  (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 5)).mpr exp_1505_lt_5

lemma exp_0351_lt_1470 : exp (0.351 : ℝ) < (1.470 : ℝ) := by
  have h := Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.351) (by norm_num : (0.351 : ℝ) ≤ 1)
    (by norm_num : (0 : ℕ) < 10)
  have h_sum_lt :
      (∑ m ∈ Finset.range 10, (0.351 : ℝ) ^ m / m.factorial) +
          (0.351 : ℝ) ^ 10 * (10 + 1) / (Nat.factorial 10 * 10) <
        (1.470 : ℝ) := by
    norm_num [Finset.range, Nat.factorial]
  exact lt_of_le_of_lt h h_sum_lt

lemma exp_1351_lt_4 : exp (1.351 : ℝ) < (4 : ℝ) := by
  rw [show (1.351 : ℝ) = 1 + 0.351 by norm_num, Real.exp_add]
  have h_mul :=
    mul_lt_mul_of_pos exp_one_lt_d9 exp_0351_lt_1470 (exp_pos 1) (by norm_num : (0 : ℝ) < 1.470)
  nlinarith [h_mul, exp_one_lt_d9, exp_0351_lt_1470]

lemma log_four_gt_1351 : (1.351 : ℝ) < log 4 :=
  (lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 4)).mpr exp_1351_lt_4

lemma exp_005_lt_115 : exp (0.05 : ℝ) < (1.15 : ℝ) := by
  have h := Real.exp_bound' (by norm_num : (0 : ℝ) ≤ 0.05) (by norm_num : (0.05 : ℝ) ≤ 1)
    (by norm_num : (0 : ℕ) < 4)
  have h_sum_lt :
      (∑ m ∈ Finset.range 4, (0.05 : ℝ) ^ m / m.factorial) +
          (0.05 : ℝ) ^ 4 * (4 + 1) / (Nat.factorial 4 * 4) <
        (1.15 : ℝ) := by
    norm_num [Finset.range, Nat.factorial]
  exact lt_of_le_of_lt h h_sum_lt

lemma growth_term_hits_zero_lt_one_point_one_five (p : FSOTParams)
    (h_hits : p.recent_hits = 0) (h_N : p.N = 1) :
    growth_term p < (1.15 : ℝ) := by
  have h_div : p.recent_hits / p.N = (0 : ℝ) := by simp [h_hits, h_N]
  have hγ : gamma_euler < (0.58 : ℝ) := by unfold gamma_euler; norm_num
  have h_arg : alpha * (1 - p.recent_hits / p.N) * gamma_euler / phi < (0.05 : ℝ) := by
    rw [h_div, sub_zero, mul_one]
    have h_prod : alpha * gamma_euler < (0.058 : ℝ) := by
      nlinarith [alpha_lt_one_tenth, alpha_pos, hγ, gamma_euler_pos]
    have hpos : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
    have hφ : (1.618 : ℝ) < phi := phi_gt_1618
    have h_upper : alpha * gamma_euler / phi < (0.058 : ℝ) / (1.618 : ℝ) := by
      rw [div_lt_div_iff₀ hpos (by norm_num : (0 : ℝ) < (1.618 : ℝ))]
      nlinarith [h_prod, hφ]
    have h_num : (0.058 : ℝ) / (1.618 : ℝ) < (0.05 : ℝ) := by norm_num
    exact lt_trans h_upper h_num
  simp only [growth_term, h_hits, h_N, zero_div]
  exact lt_trans (exp_lt_exp.mpr (by simpa [h_div, sub_zero, mul_one] using h_arg)) exp_005_lt_115

lemma cos_2208_lt_neg_055 : cos (2.208 : ℝ) < -(0.55 : ℝ) := by
  have h_eq : cos (2.208) = -cos (π - 2.208) := by
    simpa [pi_eq_real_pi] using (Real.cos_pi_sub (2.208 : ℝ)).symm
  have hpi_lo : (3.141592 : ℝ) < pi := by unfold pi; exact pi_gt_d6
  have hpi_hi : pi < (3.141593 : ℝ) := by unfold pi; exact pi_lt_d6
  have h_sub_lo : (0.933 : ℝ) < pi - 2.208 := by nlinarith [hpi_lo]
  have h_sub_hi : pi - 2.208 < (0.934 : ℝ) := by nlinarith [hpi_hi]
  have h_ref : pi - 2.208 ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_sub_lo]
    · have h_upper : pi - 2.208 ≤ π := by
        unfold pi
        linarith [h_sub_hi, pi_lt_d6]
      simpa [pi_eq_real_pi] using h_upper
  have h0934_in : (0.934 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos0934_gt_055 : (0.55 : ℝ) < cos (0.934) := by
    have h := one_sub_sq_div_two_le_cos (x := (0.934 : ℝ))
    have hnum : (0.55 : ℝ) < 1 - (0.934 : ℝ) ^ 2 / 2 := by norm_num
    linarith [h, hnum]
  have h_mono : cos (0.934) ≤ cos (π - 2.208) :=
    Real.antitoneOn_cos h_ref h0934_in (le_of_lt h_sub_hi)
  linarith [h_eq, h_mono, h_cos0934_gt_055]

lemma cos_1355_lt_0215 : cos (1.355 : ℝ) < (0.215 : ℝ) := by
  rw [cos_eq_sin_pi_div_two_sub]
  have hpi_lo : (3.141592 : ℝ) < pi := pi_gt_d6
  have hpi_hi : pi < (3.141593 : ℝ) := pi_lt_d6
  have hx : |(pi / 2 - 1.355)| ≤ 1 := by
    rw [abs_le]
    constructor <;> nlinarith [hpi_lo, hpi_hi]
  have h := sin_bound_hi hx
  have hpos : (0 : ℝ) ≤ pi / 2 - (1.355 : ℝ) := by nlinarith [hpi_lo]
  have h_abs : |pi / 2 - 1.355| = pi / 2 - 1.355 := abs_of_nonneg hpos
  have h_bound :
      sin (pi / 2 - 1.355) ≤
        pi / 2 - 1.355 - (pi / 2 - 1.355) ^ 3 / 6 + (pi / 2 - 1.355) ^ 4 * (5 / 96) := by
    simpa [h_abs] using h
  have h_x_hi : pi / 2 - 1.355 < (0.2157965 : ℝ) := by nlinarith [hpi_hi]
  have h_ref :
      (0.2157965 : ℝ) - (0.2157965 : ℝ) ^ 3 / 6 + (0.2157965 : ℝ) ^ 4 * (5 / 96) <
        (0.215 : ℝ) := by norm_num
  have h_poly_hi :
      pi / 2 - 1.355 - (pi / 2 - 1.355) ^ 3 / 6 + (pi / 2 - 1.355) ^ 4 * (5 / 96) <
        (0.215 : ℝ) := by
    refine lt_of_le_of_lt (sin_bound_poly_mono hpos (le_of_lt h_x_hi) (by norm_num)) h_ref
  linarith [h_bound, h_poly_hi]

lemma cos_1531_gt_003 : (0.03 : ℝ) < cos (1.531 : ℝ) := by
  rw [cos_eq_sin_pi_div_two_sub]
  have hpi_lo : (3.141592 : ℝ) < pi := pi_gt_d6
  have hpi_hi : pi < (3.141593 : ℝ) := pi_lt_d6
  have hx : |(pi / 2 - 1.531)| ≤ 1 := by
    rw [abs_le]
    constructor <;> nlinarith [hpi_lo, hpi_hi]
  have h := sin_bound_lo hx
  have hpos : (0 : ℝ) ≤ pi / 2 - (1.531 : ℝ) := by nlinarith [hpi_lo]
  have h_abs : |pi / 2 - 1.531| = pi / 2 - 1.531 := abs_of_nonneg hpos
  have h_x_lo : (0.039 : ℝ) < pi / 2 - 1.531 := by nlinarith [hpi_lo]
  have h_f_lo :
      (0.039 : ℝ) - (0.039 : ℝ) ^ 3 / 6 - (0.039 : ℝ) ^ 4 * (5 / 96) ≤
        pi / 2 - 1.531 - (pi / 2 - 1.531) ^ 3 / 6 - (pi / 2 - 1.531) ^ 4 * (5 / 96) := by
    refine sin_bound_poly_mono_lo (by norm_num) (le_of_lt h_x_lo) (by nlinarith [hpi_hi])
  have h_f_gt :
      (0.03 : ℝ) <
        (0.039 : ℝ) - (0.039 : ℝ) ^ 3 / 6 - (0.039 : ℝ) ^ 4 * (5 / 96) := by norm_num
  have h_sin_lo :
      (0.03 : ℝ) < sin (pi / 2 - 1.531) := by
    have h_bound :
        pi / 2 - 1.531 - (pi / 2 - 1.531) ^ 3 / 6 -
            (pi / 2 - 1.531) ^ 4 * (5 / 96) ≤ sin (pi / 2 - 1.531) := by
      simpa [h_abs] using h
    linarith [h_bound, h_f_lo, h_f_gt]
  linarith [h_sin_lo]

lemma molecular_cos_lt_neg_055 :
    cos ((psi_con + (0.4 : ℝ)) / eta_eff) < -(0.55 : ℝ) := by
  set arg := (psi_con + (0.4 : ℝ)) / eta_eff
  have h_num_lo : (1.032 : ℝ) < psi_con + (0.4 : ℝ) := by linarith [psi_con_gt_632]
  have h_num_hi : psi_con + (0.4 : ℝ) < (1.033 : ℝ) := by linarith [psi_con_lt_633]
  have h_div_lo : (1.032 : ℝ) / eta_eff < arg := div_lt_div_of_pos_right h_num_lo eta_pos
  have h_div_hi : arg < (1.033 : ℝ) / eta_eff := div_lt_div_of_pos_right h_num_hi eta_pos
  have h_eta_hi : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
  have h_eta_lo : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_mid : (1.032 : ℝ) / (0.467 : ℝ) < (1.032 : ℝ) / eta_eff := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
    exact h_eta_hi
  have h_arg_lo : (2.209 : ℝ) < arg := by
    have h_num : (2.209 : ℝ) < (1.032 : ℝ) / (0.467 : ℝ) := by norm_num
    linarith [h_div_lo, h_mid, h_num]
  have h_mid_hi : (1.033 : ℝ) / eta_eff < (1.033 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta_lo
  have h_arg_hi : arg < (2.217 : ℝ) := by
    have h_num : (1.033 : ℝ) / (0.466 : ℝ) < (2.217 : ℝ) := by norm_num
    linarith [h_div_hi, h_mid_hi, h_num]
  have h_arg_in : arg ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_arg_lo]
    · have h_upper : arg < pi := by
        have hpi : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
        linarith [h_arg_hi, hpi]
      rw [← pi_eq_real_pi]
      exact le_of_lt h_upper
  have h2208_in : (2.208 : ℝ) ∈ Set.Icc 0 π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos_arg : cos arg < cos (2.208) :=
    Real.strictAntiOn_cos h2208_in h_arg_in (by linarith [h_arg_lo])
  linarith [cos_2208_lt_neg_055, h_cos_arg]

lemma material_cos_lt_neg_075 :
    cos ((psi_con + (0.5 : ℝ)) / eta_eff) < -(0.74 : ℝ) :=
  ai_cos_lt_neg_075

lemma biological_cos_gt_003 :
    (0.03 : ℝ) < cos ((psi_con + (0.08 : ℝ)) / eta_eff) := by
  set arg := (psi_con + (0.08 : ℝ)) / eta_eff
  have h_num_lo : (0.712 : ℝ) < psi_con + (0.08 : ℝ) := by linarith [psi_con_gt_632]
  have h_num_hi : psi_con + (0.08 : ℝ) < (0.713 : ℝ) := by linarith [psi_con_lt_633]
  have h_div_lo : (0.712 : ℝ) / eta_eff < arg := div_lt_div_of_pos_right h_num_lo eta_pos
  have h_div_hi : arg < (0.713 : ℝ) / eta_eff := div_lt_div_of_pos_right h_num_hi eta_pos
  have h_eta_hi : eta_eff < (0.467 : ℝ) := eta_eff_lt_467
  have h_eta_lo : (0.466 : ℝ) < eta_eff := eta_eff_gt_466
  have h_mid : (0.712 : ℝ) / (0.467 : ℝ) < (0.712 : ℝ) / eta_eff := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) (by norm_num) eta_pos]
    exact h_eta_hi
  have h_arg_lo : (1.524 : ℝ) < arg := by
    have h_num : (1.524 : ℝ) < (0.712 : ℝ) / (0.467 : ℝ) := by norm_num
    linarith [h_div_lo, h_mid, h_num]
  have h_mid_hi : (0.713 : ℝ) / eta_eff < (0.713 : ℝ) / (0.466 : ℝ) := by
    rw [div_lt_div_iff_of_pos_left (by norm_num) eta_pos (by norm_num)]
    exact h_eta_lo
  have h_arg_hi : arg < (1.531 : ℝ) := by
    have h_num : (0.713 : ℝ) / (0.466 : ℝ) < (1.531 : ℝ) := by norm_num
    linarith [h_div_hi, h_mid_hi, h_num]
  have h_arg_in : arg ∈ Set.Icc (0 : ℝ) π := by
    constructor
    · linarith [h_arg_lo]
    · have h_upper : arg < pi := by
        have hpi : (3.1415 : ℝ) < pi := by unfold pi; exact pi_gt_d4
        linarith [h_arg_hi, hpi]
      rw [← pi_eq_real_pi]
      exact le_of_lt h_upper
  have h1531_in : (1.531 : ℝ) ∈ Set.Icc (0 : ℝ) π := by
    constructor <;> nlinarith [pi_gt_d4]
  have h_cos_arg : cos (1.531) < cos arg :=
    Real.strictAntiOn_cos h_arg_in h1531_in h_arg_hi
  linarith [cos_1531_gt_003, h_cos_arg]

lemma exp_1253_gt_34 : (3.4 : ℝ) < exp 1.253 := by
  have h_poly :
      (3.4 : ℝ) < 1 + (1.253 : ℝ) + (1.253 : ℝ) ^ 2 / 2 + (1.253 : ℝ) ^ 3 / 6 +
        (1.253 : ℝ) ^ 4 / 24 + (1.253 : ℝ) ^ 5 / 120 + (1.253 : ℝ) ^ 6 / 720 := by norm_num
  have h_sum := Real.sum_le_exp_of_nonneg (by norm_num : (0 : ℝ) ≤ 1.253) 7
  have h_eq :
      (1 + (1.253 : ℝ) + (1.253 : ℝ) ^ 2 / 2 + (1.253 : ℝ) ^ 3 / 6 + (1.253 : ℝ) ^ 4 / 24 +
          (1.253 : ℝ) ^ 5 / 120 + (1.253 : ℝ) ^ 6 / 720 : ℝ) =
        ∑ i ∈ Finset.range 7, (1.253 : ℝ) ^ i / Nat.factorial i := by
    norm_num [Finset.range, Nat.factorial]
  linarith [h_poly, h_eq, h_sum]

lemma log_34_lt_1253 : log 3.4 < (1.253 : ℝ) :=
  (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 3.4)).2 exp_1253_gt_34

lemma molecular_exp_factor_gt_34 :
    (3.4 : ℝ) < exp (1 + bleed_in_factor * (0.4 : ℝ)) := by
  have h_bleed : (1.253 : ℝ) < 1 + bleed_in_factor * (0.4 : ℝ) := by
    nlinarith [bleed_in_factor_gt_0773]
  have h_log : log 3.4 < 1 + bleed_in_factor * (0.4 : ℝ) := lt_trans log_34_lt_1253 h_bleed
  exact (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 3.4)).1 h_log

lemma biological_exp_factor_gt_two :
    (2 : ℝ) < exp (1 + bleed_in_factor * (0.08 : ℝ)) := by
  have h_arg : (1 : ℝ) < 1 + bleed_in_factor * (0.08 : ℝ) := by
    nlinarith [bleed_in_factor_gt_0773]
  have h_exp1 : (2 : ℝ) < exp 1 := by linarith [exp_one_gt_d9]
  exact lt_trans h_exp1 (exp_lt_exp.mpr h_arg)

lemma sqrt_10_lt_3163 : sqrt (10 : ℝ) < (3.163 : ℝ) := by
  have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (10 : ℝ) < (3.163 : ℝ) ^ 2)
  simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ (3.163 : ℝ))] using h

lemma sqrt_12_lt_3465 : sqrt (12 : ℝ) < (3.465 : ℝ) := by
  have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (12 : ℝ) < (3.465 : ℝ) ^ 2)
  simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ (3.465 : ℝ))] using h

lemma sqrt_12_gt_3463 : (3.463 : ℝ) < sqrt (12 : ℝ) := by
  exact Real.lt_sqrt_of_sq_lt (by norm_num : (3.463 : ℝ) ^ 2 < 12)

lemma growth_term_coherence_product_lt_11523 (p : FSOTParams)
    (h_hits : p.recent_hits = 0) (h_N : p.N = 1) :
    growth_term p * coherence_efficiency < (1.1523 : ℝ) := by
  have h_g := growth_term_hits_zero_lt_one_point_one_five p h_hits h_N
  have h_g_pos : (0 : ℝ) < growth_term p := by
    dsimp [growth_term]
    exact exp_pos _
  have h_mul :=
    mul_lt_mul_of_pos h_g coherence_efficiency_lt_1002 h_g_pos (by norm_num : (0 : ℝ) < 1.002)
  have h_eq : (1.15 : ℝ) * (1.002 : ℝ) = (1.1523 : ℝ) := by norm_num
  rw [← h_eq]
  exact h_mul

lemma omega_abs_ge_one : (1 : ℝ) ≤ abs omega := by
  dsimp [omega]
  rw [abs_mul]
  have hsin : (0.91385 : ℝ) < sin (pi / e) := sin_pi_div_e_gt_91385
  have hsin_pos : (0 : ℝ) < sin (pi / e) := by linarith [hsin]
  have hsqrt : (1.414 : ℝ) < sqrt2 := by unfold sqrt2; exact Real.lt_sqrt_of_sq_lt (by norm_num)
  have hsqrt_pos : (0 : ℝ) < sqrt2 := by unfold sqrt2; exact Real.sqrt_pos.mpr (by norm_num)
  rw [abs_of_pos hsin_pos, abs_of_pos hsqrt_pos]
  nlinarith [hsin, hsqrt]

lemma gamma_abs_eq : abs gamma = log 2 / phi := by
  unfold gamma
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have h_log2_pos : (0 : ℝ) < log 2 := log_pos (by norm_num : (1 : ℝ) < 2)
  rw [abs_div, abs_neg, abs_of_pos h_log2_pos, abs_of_pos hφ]

lemma chaos_factor_abs_lt_one : abs chaos_factor < (1 : ℝ) := by
  unfold chaos_factor
  have hω_abs : (0 : ℝ) < abs omega :=
    lt_of_lt_of_le (by norm_num : (0 : ℝ) < (1 : ℝ)) omega_abs_ge_one
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  have h_log2 : log 2 < (1 : ℝ) := by
    exact (log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 2)).2 (by linarith [exp_one_gt_d9])
  rw [abs_div, gamma_abs_eq]
  refine (div_lt_iff₀ hω_abs).mpr ?_
  refine (div_lt_iff₀ hφ).mpr ?_
  nlinarith [h_log2, phi_gt_one, omega_abs_ge_one]

lemma D_eff_shift_abs_le (p : FSOTParams) (h_D : (6 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 25) :
    abs (p.D_eff - 25) ≤ (19 : ℝ) := by
  rw [abs_le]
  constructor
  · have h_lo : (6 : ℝ) - 25 ≤ p.D_eff - 25 := by linarith [h_D.1]
    linarith [h_lo]
  · have h_hi : p.D_eff - 25 ≤ (0 : ℝ) := by linarith [h_D.2]
    linarith [h_hi]

lemma chaos_perturbation_abs_le_two (p : FSOTParams) (h_D : (6 : ℝ) ≤ p.D_eff ∧ p.D_eff ≤ 25) :
    abs (1 + chaos_factor * (p.D_eff - 25) / 25) ≤ (2 : ℝ) := by
  have h_shift := D_eff_shift_abs_le p h_D
  have h_frac : abs ((p.D_eff - 25) / 25) ≤ (19 / 25 : ℝ) := by
    have hpos : (0 : ℝ) < (25 : ℝ) := by norm_num
    rw [abs_div, abs_of_pos hpos]
    refine (div_le_iff₀ hpos).mpr ?_
    linarith [h_shift]
  have h_prod : abs (chaos_factor * (p.D_eff - 25) / 25) < (1 : ℝ) := by
    have h_cf : abs chaos_factor < (1 : ℝ) := chaos_factor_abs_lt_one
    have h_frac_lt : abs ((p.D_eff - 25) / 25) < (1 : ℝ) := by nlinarith [h_frac]
    have h_mul : abs chaos_factor * abs ((p.D_eff - 25) / 25) < (1 : ℝ) := by
      nlinarith [h_cf, h_frac_lt, abs_nonneg chaos_factor, abs_nonneg ((p.D_eff - 25) / 25)]
    have h_rearr : chaos_factor * (p.D_eff - 25) / 25 =
        chaos_factor * ((p.D_eff - 25) / 25) := by ring
    rw [h_rearr, abs_mul]
    exact h_mul
  have h_tri := abs_add_le 1 (chaos_factor * (p.D_eff - 25) / 25)
  nlinarith [h_tri, h_prod]

end

end FSOT.Formal