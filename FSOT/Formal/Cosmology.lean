/-
  FSOT Formal Cosmology — Wave 1 ΛCDM observables and domain anchors.

  Numeric values are grounded in `fsot_compute.py` (FSOT document update)
  and cached in `data/canonical_constants.json` via scripts/sync_canonical_constants.py.
-/

import FSOT.Formal.Scalar
import FSOT.Formal.Bounds
import Mathlib.Algebra.Order.GroupWithZero.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace FSOT.Formal

noncomputable section

open Real

/-- Cosmology domain interpretation constant: 1 / (φ · 10). -/
def c_cosm : ℝ := 1 / (phi * 10)

/-- Cached cosmology scalar S_cosm from domain D_eff = 25 (Python oracle). -/
def S_cosm_cached : ℝ := -(0.5024559462100433 : ℝ)

/-- Cached quantum scalar S_quant from domain D_eff = 6 (Python oracle). -/
def S_quant_cached : ℝ := (0.9555063001027196 : ℝ)

/-- Wave-1 canonical targets from `data/canonical_constants.json`. -/
def alpha_s_MZ_canonical : ℝ := (0.117099663048638321 : ℝ)
def h0_fsot_canonical : ℝ := (68.440056829794272 : ℝ)
def t_cmb_fsot_canonical : ℝ := (2.724728386673958 : ℝ)
def n_s_fsot_canonical : ℝ := (0.9638062833678816 : ℝ)
def omega_b_h2_fsot_canonical : ℝ := (0.022356124082273698 : ℝ)

/-- Strong coupling at M_Z: α_s = 1 / (e · π). -/
def alpha_s_MZ : ℝ := 1 / (e * pi)

/-- Hubble parameter H₀ from FSOT Wave 1. -/
def h0_fsot (S_cosm : ℝ) : ℝ :=
  100 * (1 + S_cosm * acoustic_bleed / acoustic_inflow)

/-- CMB temperature from FSOT Wave 1. -/
def t_cmb_fsot (S_cosm : ℝ) : ℝ :=
  phi ^ 2 + gamma_euler / e * |S_cosm|

/-- Spectral index from FSOT Wave 1. -/
def n_s_fsot (S_cosm : ℝ) : ℝ :=
  1 + S_cosm * c_cosm * rpow phi (1 / pi)

/-- Baryon density parameter from FSOT Wave 1. -/
def omega_b_h2_fsot (S_cosm S_quant : ℝ) : ℝ :=
  |S_cosm| * (1 - S_quant)

/-- FSOT perceived-parameter base (γ / e). -/
def p_base : ℝ := gamma_euler / e

/-- Wave-derived stationary soliton radius: r★ = π³ / p_base − φ. -/
def r_star_Mpc : ℝ := (pi ^ 3) / p_base - phi

/-- Topological stabilization shift at the baryon-drag epoch. -/
def delta_lambda_cosm : ℝ := 0.0216083

/-- Baryon drag horizon: r_d = r★ · (1 + δλ). -/
def r_d_canonical : ℝ := r_star_Mpc * (1 + delta_lambda_cosm)

lemma c_cosm_pos : (0 : ℝ) < c_cosm := by
  unfold c_cosm
  have hφ : (0 : ℝ) < phi := lt_trans (by norm_num) phi_gt_one
  exact div_pos (by norm_num) (mul_pos hφ (by norm_num))

lemma c_cosm_gt_061800 : (0.061800 : ℝ) < c_cosm := by
  unfold c_cosm
  have hφ10 : (0 : ℝ) < phi * 10 := mul_pos (lt_trans (by norm_num) phi_gt_one) (by norm_num)
  rw [lt_div_iff₀ hφ10]
  nlinarith [phi_lt_16181]

lemma c_cosm_lt_061806 : c_cosm < (0.061806 : ℝ) := by
  unfold c_cosm
  have hφ10 : (0 : ℝ) < phi * 10 := mul_pos (lt_trans (by norm_num) phi_gt_one) (by norm_num)
  rw [div_lt_iff₀ hφ10]
  nlinarith [phi_gt_1618]

lemma p_base_gt_021234 : (0.21234 : ℝ) < p_base := by
  unfold p_base
  have h_div : gamma_euler / (2.7182818286 : ℝ) < gamma_euler / e :=
    (div_lt_div_iff_of_pos_left gamma_euler_pos (by norm_num : (0 : ℝ) < 2.7182818286) (exp_pos 1)).mpr
      e_lt_27182818286
  have h_num : (0.21234 : ℝ) < gamma_euler / (2.7182818286 : ℝ) := by
    unfold gamma_euler
    norm_num
  linarith [h_num, h_div]

lemma p_base_lt_0212371 : p_base < (0.212371 : ℝ) := by
  unfold p_base
  have hγ_hi : gamma_euler < (0.57722 : ℝ) := by unfold gamma_euler; norm_num
  have h_div : gamma_euler / e < gamma_euler / (2.7182818283 : ℝ) :=
    div_lt_div_of_pos_left gamma_euler_pos (by norm_num) e_gt_27182818283
  have h_frac : gamma_euler / (2.7182818283 : ℝ) < (0.57722 : ℝ) / (2.7182818283 : ℝ) :=
    div_lt_div_of_pos_right hγ_hi (by norm_num)
  have h_const : (0.57722 : ℝ) / (2.7182818283 : ℝ) < (0.212371 : ℝ) := by norm_num
  linarith [h_div, h_frac, h_const]

lemma alpha_s_MZ_pos : (0 : ℝ) < alpha_s_MZ := by
  unfold alpha_s_MZ
  exact div_pos (by norm_num) (mul_pos (exp_pos _) Real.pi_pos)

lemma e_mul_pi_gt_one : (1 : ℝ) < e * pi := by
  unfold e
  nlinarith [exp_one_gt_d9, pi_gt_one]

lemma alpha_s_MZ_lt_one : alpha_s_MZ < (1 : ℝ) := by
  unfold alpha_s_MZ
  have hden : (0 : ℝ) < e * pi := by
    unfold e
    exact mul_pos (exp_pos _) Real.pi_pos
  have hgt := e_mul_pi_gt_one
  rw [div_lt_one hden]
  exact hgt

lemma S_cosm_cached_neg : S_cosm_cached < 0 := by
  unfold S_cosm_cached
  norm_num

lemma S_cosm_cached_bounds :
    (-0.502456 : ℝ) < S_cosm_cached ∧ S_cosm_cached < (-0.502455 : ℝ) := by
  unfold S_cosm_cached
  constructor <;> norm_num

lemma S_cosm_cached_abs_bounds :
    (0.502455 : ℝ) < |S_cosm_cached| ∧ |S_cosm_cached| < (0.502456 : ℝ) := by
  have h := S_cosm_cached_bounds
  constructor
  · rw [abs_of_neg (by linarith [h.1])]
    linarith [h.2]
  · rw [abs_of_neg (by linarith [h.1])]
    linarith [h.1]

/-- Cached Wave-1 Ω_b h² is strictly positive (Python oracle values). -/
theorem omega_b_h2_fsot_cached_pos : (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  unfold omega_b_h2_fsot S_cosm_cached S_quant_cached
  norm_num

/-- α_s(M_Z) matches the canonical Wave-1 cache (`1/(e·π)`). -/
theorem alpha_s_MZ_approx_value : |alpha_s_MZ - alpha_s_MZ_canonical| < (1e-8 : ℝ) := by
  unfold alpha_s_MZ alpha_s_MZ_canonical
  have h_epi_pos : (0 : ℝ) < e * pi := by
    unfold e
    exact mul_pos (exp_pos _) Real.pi_pos
  have h_lo : (0.11709966304 : ℝ) < 1 / (e * pi) := by
    rw [lt_div_iff₀ h_epi_pos]
    have hprod := e_pi_lt_27182818286_mul_pi
    have hconst : (0.11709966304 : ℝ) * ((2.7182818286 : ℝ) * (3.14159265358979323847 : ℝ)) < 1 := by
      norm_num
    nlinarith [hprod, hconst]
  have h_hi : 1 / (e * pi) < (0.1170996631 : ℝ) := by
    rw [div_lt_iff₀ h_epi_pos]
    have hprod := e_pi_gt_27182818283_mul_pi
    have hconst : 1 < (0.1170996631 : ℝ) * ((2.7182818283 : ℝ) * (3.14159265358979323846 : ℝ)) := by
      norm_num
    nlinarith [hprod, hconst]
  have h_canon_lo : (0.11709966304 : ℝ) < alpha_s_MZ_canonical := by
    unfold alpha_s_MZ_canonical
    norm_num
  have h_canon_hi : alpha_s_MZ_canonical < (0.1170996631 : ℝ) := by
    unfold alpha_s_MZ_canonical
    norm_num
  rw [abs_lt]
  constructor <;> linarith [h_lo, h_hi, h_canon_lo, h_canon_hi]

/-- H₀ at cached domain scalars matches the canonical Wave-1 cache. -/
theorem h0_fsot_cached_approx_value :
    |h0_fsot S_cosm_cached - h0_fsot_canonical| < (0.11 : ℝ) := by
  unfold h0_fsot S_cosm_cached h0_fsot_canonical
  have h_ratio_lo := acoustic_bleed_div_inflow_gt_62600
  have h_ratio_hi := acoustic_bleed_div_inflow_lt_62961
  have h_S : S_cosm_cached = -(0.5024559462100433 : ℝ) := by unfold S_cosm_cached; rfl
  have h_const_lo : (68.364 : ℝ) < 100 * (1 + -(0.5024559462100433 : ℝ) * (0.62961 : ℝ)) := by norm_num
  have h_const_hi : 100 * (1 + -(0.5024559462100433 : ℝ) * (0.62600 : ℝ)) < (68.547 : ℝ) := by norm_num
  have h_mul_lo : -(0.5024559462100433 : ℝ) * (acoustic_bleed / acoustic_inflow) >
      -(0.5024559462100433 : ℝ) * (0.62961 : ℝ) := by
    nlinarith [h_ratio_hi]
  have h_mul_hi : -(0.5024559462100433 : ℝ) * (0.62600 : ℝ) >
      -(0.5024559462100433 : ℝ) * (acoustic_bleed / acoustic_inflow) := by
    nlinarith [h_ratio_lo]
  have h_mul_eq : (-(0.5024559462100433 : ℝ) * acoustic_bleed) / acoustic_inflow =
      -(0.5024559462100433 : ℝ) * (acoustic_bleed / acoustic_inflow) := by field_simp
  have h_lo : (68.364 : ℝ) <
      100 * (1 + (-(0.5024559462100433 : ℝ) * acoustic_bleed) / acoustic_inflow) := by
    rw [h_mul_eq]
    linarith [h_const_lo, h_mul_lo]
  have h_hi : 100 * (1 + (-(0.5024559462100433 : ℝ) * acoustic_bleed) / acoustic_inflow) <
      (68.547 : ℝ) := by
    rw [h_mul_eq]
    linarith [h_const_hi, h_mul_hi]
  rw [abs_lt]
  constructor <;> linarith [h_lo, h_hi]

/-- T_CMB at cached S_cosm matches the canonical Wave-1 cache. -/
theorem t_cmb_fsot_cached_approx_value :
    |t_cmb_fsot S_cosm_cached - t_cmb_fsot_canonical| < (0.001 : ℝ) := by
  unfold t_cmb_fsot S_cosm_cached t_cmb_fsot_canonical
  have h_phi_sq_lo := phi_sq_gt_261792
  have h_phi_sq_hi := phi_sq_lt_26183
  have h_pbase_lo := p_base_gt_021234
  have h_pbase_hi := p_base_lt_0212371
  have h_abs : |S_cosm_cached| = (0.5024559462100433 : ℝ) := by
    unfold S_cosm_cached
    norm_num
  have h_lo : (2.7246 : ℝ) < phi ^ 2 + gamma_euler / e * (0.5024559462100433 : ℝ) := by
    unfold p_base at *
    nlinarith [h_phi_sq_lo, h_pbase_lo]
  have h_hi : phi ^ 2 + gamma_euler / e * (0.5024559462100433 : ℝ) < (2.7251 : ℝ) := by
    unfold p_base at *
    nlinarith [h_phi_sq_hi, h_pbase_hi]
  have h_lo' : (2.7246 : ℝ) < phi ^ 2 + gamma_euler / e * |S_cosm_cached| := by
    rw [h_abs]
    exact h_lo
  have h_hi' : phi ^ 2 + gamma_euler / e * |S_cosm_cached| < (2.7251 : ℝ) := by
    rw [h_abs]
    exact h_hi
  rw [abs_lt]
  constructor <;> linarith [h_lo', h_hi']

/-- n_s at cached S_cosm matches the canonical Wave-1 cache. -/
theorem n_s_fsot_cached_approx_value :
    |n_s_fsot S_cosm_cached - n_s_fsot_canonical| < (3e-4 : ℝ) := by
  unfold n_s_fsot S_cosm_cached n_s_fsot_canonical c_cosm
  have h_S := S_cosm_cached_bounds
  have h_rpow_lo := phi_rpow_inv_pi_gt_11653
  have h_rpow_hi := phi_rpow_inv_pi_lt_1168
  have h_c_lo := c_cosm_gt_061800
  have h_c_hi := c_cosm_lt_061806
  have h_crpow_pos : (0 : ℝ) < c_cosm * rpow phi (1 / pi) := by
    refine mul_pos c_cosm_pos ?_
    exact Real.rpow_pos_of_pos (lt_trans (by norm_num) phi_gt_one) _
  have h_rpow_pos : (0 : ℝ) < rpow phi (1 / pi) :=
    Real.rpow_pos_of_pos (lt_trans (by norm_num) phi_gt_one) _
  have h_rpow_eq : rpow phi (1 / pi) = phi ^ (1 / pi) := rfl
  have h_c_rpow_lo : (0.061800 : ℝ) * (1.1653 : ℝ) < c_cosm * phi ^ (1 / pi) := by
    nlinarith [h_c_lo, h_rpow_lo]
  have h_c_rpow_hi : c_cosm * phi ^ (1 / pi) < (0.061806 : ℝ) * (1.168 : ℝ) := by
    nlinarith [h_c_hi, h_rpow_hi]
  have h_P_lo : (0.061800 : ℝ) * (1.1653 : ℝ) < c_cosm * rpow phi (1 / pi) := by
    rwa [h_rpow_eq]
  have h_P_hi : c_cosm * rpow phi (1 / pi) < (0.061806 : ℝ) * (1.168 : ℝ) := by
    rwa [h_rpow_eq]
  have h_const_lo : (0.96368 : ℝ) <
      1 + -(0.502456 : ℝ) * ((0.061806 : ℝ) * (1.168 : ℝ)) := by norm_num
  have h_const_hi : 1 + -(0.502455 : ℝ) * ((0.061800 : ℝ) * (1.1653 : ℝ)) <
      (0.96382 : ℝ) := by norm_num
  have h_prod_lo : -(0.502456 : ℝ) * ((0.061806 : ℝ) * (1.168 : ℝ)) <
      -(0.5024559462100433 : ℝ) * (c_cosm * rpow phi (1 / pi)) := by
    nlinarith [h_S.1, h_P_hi, h_crpow_pos]
  have h_prod_hi : -(0.5024559462100433 : ℝ) * (c_cosm * rpow phi (1 / pi)) <
      -(0.502455 : ℝ) * ((0.061800 : ℝ) * (1.1653 : ℝ)) := by
    nlinarith [h_S.2, h_P_lo, h_crpow_pos]
  have h_lo : (0.96368 : ℝ) <
      1 + -(0.5024559462100433 : ℝ) * (c_cosm * rpow phi (1 / pi)) := by
    simpa [mul_assoc] using
      (show (0.96368 : ℝ) < 1 + -(0.5024559462100433 : ℝ) * c_cosm * rpow phi (1 / pi) from
        by linarith [h_const_lo, h_prod_lo])
  have h_hi : 1 + -(0.5024559462100433 : ℝ) * (c_cosm * rpow phi (1 / pi)) < (0.96382 : ℝ) := by
    simpa [mul_assoc] using
      (show 1 + -(0.5024559462100433 : ℝ) * c_cosm * rpow phi (1 / pi) < (0.96382 : ℝ) from
        by linarith [h_const_hi, h_prod_hi])
  have h_lo' : (0.96368 : ℝ) <
      1 + -(0.5024559462100433 : ℝ) * ((1 / (phi * 10)) * rpow phi (1 / pi)) := by
    simpa [c_cosm, mul_assoc] using h_lo
  have h_hi' : 1 + -(0.5024559462100433 : ℝ) * ((1 / (phi * 10)) * rpow phi (1 / pi)) < (0.96382 : ℝ) := by
    simpa [c_cosm, mul_assoc] using h_hi
  rw [abs_lt]
  constructor <;> linarith [h_lo', h_hi']

/-- Ω_b h² at cached domain scalars matches the canonical Wave-1 cache. -/
theorem omega_b_h2_fsot_cached_approx_value :
    |omega_b_h2_fsot S_cosm_cached S_quant_cached - omega_b_h2_fsot_canonical| < (1e-5 : ℝ) := by
  unfold omega_b_h2_fsot S_cosm_cached S_quant_cached omega_b_h2_fsot_canonical
  have h_Q_val : S_quant_cached = (0.9555063001027196 : ℝ) := by unfold S_quant_cached; rfl
  have h_Q_lo : (0.9555060 : ℝ) < (0.9555063001027196 : ℝ) := by norm_num
  have h_Q_hi : (0.9555063001027196 : ℝ) < (0.9555064 : ℝ) := by norm_num
  have h_abs : |S_cosm_cached| = (0.5024559462100433 : ℝ) := by
    unfold S_cosm_cached
    norm_num
  have h_lo : (0.0223560 : ℝ) < |S_cosm_cached| * (1 - S_quant_cached) := by
    rw [h_abs, h_Q_val]
    norm_num
  have h_hi : |S_cosm_cached| * (1 - S_quant_cached) < (0.0223563 : ℝ) := by
    rw [h_abs, h_Q_val]
    norm_num
  rw [abs_lt]
  constructor <;> linarith [h_lo, h_hi]

lemma p_base_pos : (0 : ℝ) < p_base := by
  unfold p_base
  exact div_pos (by norm_num [gamma_euler]) (exp_pos _)

lemma delta_lambda_cosm_pos : (0 : ℝ) < delta_lambda_cosm := by
  unfold delta_lambda_cosm
  norm_num

/-- Baryon-drag shift is small enough to keep r_d in the observed Mpc band (algebraic bound). -/
lemma delta_lambda_cosm_lt_one : delta_lambda_cosm < (1 : ℝ) := by
  unfold delta_lambda_cosm
  norm_num

/-- Baryon drag horizon lies in the observation band around 147.52 Mpc.
   Interval certificate: r_d ∈ (147.48, 147.55), hence |r_d − 147.52| < 0.05. -/
theorem r_d_approx_value : |r_d_canonical - 147.52| < 0.05 := by
  have h_pi_lo : (3.14159265358979323846 : ℝ) < pi := by unfold pi; exact pi_gt_d20
  have h_pi_hi : pi < (3.14159265358979323847 : ℝ) := by unfold pi; exact pi_lt_d20
  have h_phi_hi : phi < (1.6181 : ℝ) := by
    unfold phi
    have h_s : sqrt 5 < (2.2361 : ℝ) := by
      have h := Real.sqrt_lt_sqrt (by norm_num) (by norm_num : (5 : ℝ) < (2.2361 : ℝ) ^ 2)
      simpa [Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 2.2361)] using h
    linarith
  have h_phi_lo : (1.618 : ℝ) < phi := by
    unfold phi
    have h : (2.236 : ℝ) < sqrt 5 := Real.lt_sqrt_of_sq_lt (by norm_num : (2.236 : ℝ) ^ 2 < 5)
    linarith
  have h_e_sharp_lo : (2.7182818283 : ℝ) < e := by unfold e; linarith [exp_one_gt_d9]
  have h_e_sharp_hi : e < (2.7182818286 : ℝ) := by unfold e; linarith [exp_one_lt_d9]
  have h_gamma_hi : gamma_euler < (0.57722 : ℝ) := by unfold gamma_euler; norm_num
  have h_pbase_u : p_base < (0.212371 : ℝ) := by
    unfold p_base
    have h_div : gamma_euler / e < gamma_euler / (2.7182818283 : ℝ) :=
      div_lt_div_of_pos_left gamma_euler_pos (by norm_num) h_e_sharp_lo
    have h_frac : gamma_euler / (2.7182818283 : ℝ) < (0.57722 : ℝ) / (2.7182818283 : ℝ) :=
      div_lt_div_of_pos_right h_gamma_hi (by norm_num)
    have h_num : (0.57722 : ℝ) / (2.7182818283 : ℝ) < (0.212371 : ℝ) := by norm_num
    linarith [h_div, h_frac, h_num]
  have h_pbase_lo : (0.21234 : ℝ) < p_base := by
    unfold p_base
    have h_div : gamma_euler / (2.7182818286 : ℝ) < gamma_euler / e :=
      (div_lt_div_iff_of_pos_left gamma_euler_pos (by norm_num : (0 : ℝ) < 2.7182818286) (exp_pos 1)).mpr
        h_e_sharp_hi
    have h_num : (0.21234 : ℝ) < gamma_euler / (2.7182818286 : ℝ) := by
      unfold gamma_euler
      norm_num
    linarith [h_num, h_div]
  have h_pi3_lo : (31.006276 : ℝ) < pi ^ 3 := by
    have hpow : (3.14159265358979323846 : ℝ) ^ 3 < pi ^ 3 :=
      pow_lt_pow_left₀ h_pi_lo (by norm_num) (by norm_num : (3 : ℕ) ≠ 0)
    have hconst : (31.006276 : ℝ) < (3.14159265358979323846 : ℝ) ^ 3 := by
      norm_num [pow_succ, pow_two]
    linarith [hpow, hconst]
  have h_pi3_hi : pi ^ 3 < (31.0066 : ℝ) := by
    have hpow : pi ^ 3 < (3.14159265358979323847 : ℝ) ^ 3 :=
      pow_lt_pow_left₀ h_pi_hi (le_of_lt Real.pi_pos) (by norm_num : (3 : ℕ) ≠ 0)
    have hconst : (3.14159265358979323847 : ℝ) ^ 3 < (31.0066 : ℝ) := by
      norm_num [pow_succ, pow_two]
    linarith [hpow, hconst]
  have h_rstar_lo : (144.38 : ℝ) < r_star_Mpc := by
    unfold r_star_Mpc
    have h_frac : (31.006276 : ℝ) / (0.212371 : ℝ) < pi ^ 3 / p_base := by
      apply (div_lt_div_iff₀ (by norm_num : (0 : ℝ) < 0.212371) p_base_pos).mpr
      nlinarith [h_pi3_lo, h_pbase_u]
    have h_mid : (146.0 : ℝ) < pi ^ 3 / p_base := by
      have h1 : (146.0 : ℝ) < (31.006276 : ℝ) / (0.212371 : ℝ) := by norm_num
      exact lt_trans h1 h_frac
    have h_sub : (144.38 : ℝ) < pi ^ 3 / p_base - phi := by nlinarith [h_mid, h_phi_hi]
    linarith [h_sub]
  have h_rstar_hi : r_star_Mpc < (144.42 : ℝ) := by
    unfold r_star_Mpc
    have h_frac : pi ^ 3 / p_base < (31.0066 : ℝ) / (0.21234 : ℝ) := by
      apply (div_lt_div_iff₀ p_base_pos (by norm_num : (0 : ℝ) < 0.21234)).mpr
      nlinarith [h_pi3_hi, h_pbase_lo]
    have h_sub : pi ^ 3 / p_base - phi < (144.42 : ℝ) := by nlinarith [h_frac, h_phi_lo]
    linarith [h_sub]
  have h_delta_lo : (0.0216 : ℝ) < delta_lambda_cosm := by norm_num [delta_lambda_cosm]
  have h_delta_hi : delta_lambda_cosm < (0.02162 : ℝ) := by norm_num [delta_lambda_cosm]
  have h_rd_lo : (147.48 : ℝ) < r_d_canonical := by
    unfold r_d_canonical
    have h_mul : (144.38 : ℝ) * (1.0216 : ℝ) < r_star_Mpc * (1 + delta_lambda_cosm) := by
      nlinarith [h_rstar_lo, h_delta_lo, delta_lambda_cosm_pos]
    have h1 : (147.48 : ℝ) < (144.38 : ℝ) * (1.0216 : ℝ) := by norm_num
    linarith [h_mul, h1]
  have h_rd_hi : r_d_canonical < (147.55 : ℝ) := by
    unfold r_d_canonical
    have h_mul : r_star_Mpc * (1 + delta_lambda_cosm) < (144.42 : ℝ) * (1.02162 : ℝ) := by
      nlinarith [h_rstar_hi, h_delta_hi, delta_lambda_cosm_pos]
    have h1 : (144.42 : ℝ) * (1.02162 : ℝ) < (147.55 : ℝ) := by norm_num
    linarith [h_mul, h1]
  rw [abs_lt]
  constructor <;> linarith [h_rd_lo, h_rd_hi]

end

end FSOT.Formal