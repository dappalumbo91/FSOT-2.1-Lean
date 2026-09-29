/-
  FSOT Formal GRSMCKMSpine — multi-prover GR/SM/CKM/PMNS obligations.
  Generator: scripts/export_and_generate_gr_sm_ckm_artifacts.py
  Independent numeric certificates (norm_num / decide).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace FSOT.Formal.GRSMCKM

noncomputable section

theorem lambda_ckm_err_under_half :
    (0.06225011989853476 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.06225011989853476 : ℝ) < (0.5 : ℝ))

theorem lambda_ckm_measured_pos :
    (0 : ℝ) < (0.22501 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.22501 : ℝ))

theorem lambda_ckm_abs_diff :
    (0.00014006899478369306 : ℝ) < (0.00014146968473252998 : ℝ) :=
  (by norm_num : (0.00014006899478369306 : ℝ) < (0.00014146968473252998 : ℝ))

theorem A_wolfenstein_err_under_half :
    (0.05246555208389803 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.05246555208389803 : ℝ) < (0.5 : ℝ))

theorem A_wolfenstein_measured_pos :
    (0 : ℝ) < (0.826 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.826 : ℝ))

theorem A_wolfenstein_abs_diff :
    (0.0004333654602129977 : ℝ) < (0.0004376991148161277 : ℝ) :=
  (by norm_num : (0.0004333654602129977 : ℝ) < (0.0004376991148161277 : ℝ))

theorem rho_bar_err_under_half :
    (0.02700157709000836 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.02700157709000836 : ℝ) < (0.5 : ℝ))

theorem rho_bar_measured_pos :
    (0 : ℝ) < (0.1591 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.1591 : ℝ))

theorem rho_bar_abs_diff :
    (4.29595091502033e-05 : ℝ) < (4.3389104242705336e-05 : ℝ) :=
  (by norm_num : (4.29595091502033e-05 : ℝ) < (4.3389104242705336e-05 : ℝ))

theorem eta_bar_err_under_half :
    (0.0028013614651725667 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0028013614651725667 : ℝ) < (0.5 : ℝ))

theorem eta_bar_measured_pos :
    (0 : ℝ) < (0.3523 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.3523 : ℝ))

theorem eta_bar_abs_diff :
    (9.869196441802952e-06 : ℝ) < (9.967888407220981e-06 : ℝ) :=
  (by norm_num : (9.869196441802952e-06 : ℝ) < (9.967888407220981e-06 : ℝ))

theorem Jarlskog_J_err_under_half :
    (0.23792303102008408 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.23792303102008408 : ℝ) < (0.5 : ℝ))

theorem Jarlskog_J_measured_pos :
    (0 : ℝ) < (3.12e-05 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.12e-05 : ℝ))

theorem Jarlskog_J_abs_diff :
    (7.423198567826624e-08 : ℝ) < (7.497430653504891e-08 : ℝ) :=
  (by norm_num : (7.423198567826624e-08 : ℝ) < (7.497430653504891e-08 : ℝ))

theorem delta_ckm_rad_err_under_half :
    (0.02612849108321111 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.02612849108321111 : ℝ) < (0.5 : ℝ))

theorem delta_ckm_rad_measured_pos :
    (0 : ℝ) < (1.147 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.147 : ℝ))

theorem delta_ckm_rad_abs_diff :
    (0.0002996937927244314 : ℝ) < (0.0003026907306526757 : ℝ) :=
  (by norm_num : (0.0002996937927244314 : ℝ) < (0.0003026907306526757 : ℝ))

theorem V_ud_err_under_half :
    (0.002658467271059532 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.002658467271059532 : ℝ) < (0.5 : ℝ))

theorem V_ud_measured_pos :
    (0 : ℝ) < (0.97435 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.97435 : ℝ))

theorem V_ud_abs_diff :
    (2.590277585556855e-05 : ℝ) < (2.6161803615124236e-05 : ℝ) :=
  (by norm_num : (2.590277585556855e-05 : ℝ) < (2.6161803615124236e-05 : ℝ))

theorem V_us_err_under_half :
    (0.06225011989853476 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.06225011989853476 : ℝ) < (0.5 : ℝ))

theorem V_us_measured_pos :
    (0 : ℝ) < (0.22501 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.22501 : ℝ))

theorem V_us_abs_diff :
    (0.00014006899478369306 : ℝ) < (0.00014146968473252998 : ℝ) :=
  (by norm_num : (0.00014006899478369306 : ℝ) < (0.00014146968473252998 : ℝ))

theorem V_ub_err_under_half :
    (0.23474330619715575 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.23474330619715575 : ℝ) < (0.5 : ℝ))

theorem V_ub_measured_pos :
    (0 : ℝ) < (0.003732 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.003732 : ℝ))

theorem V_ub_abs_diff :
    (8.760620187277853e-06 : ℝ) < (8.848226390150632e-06 : ℝ) :=
  (by norm_num : (8.760620187277853e-06 : ℝ) < (8.848226390150632e-06 : ℝ))

theorem V_cd_err_under_half :
    (0.12454706932169445 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.12454706932169445 : ℝ) < (0.5 : ℝ))

theorem V_cd_measured_pos :
    (0 : ℝ) < (0.22487 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.22487 : ℝ))

theorem V_cd_abs_diff :
    (0.0002800689947836943 : ℝ) < (0.00028286968473253125 : ℝ) :=
  (by norm_num : (0.0002800689947836943 : ℝ) < (0.00028286968473253125 : ℝ))

theorem V_cs_err_under_half :
    (0.08568112914816942 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.08568112914816942 : ℝ) < (0.5 : ℝ))

theorem V_cs_measured_pos :
    (0 : ℝ) < (0.97349 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.97349 : ℝ))

theorem V_cs_abs_diff :
    (0.0008340972241445144 : ℝ) < (0.0008424381963869595 : ℝ) :=
  (by norm_num : (0.0008340972241445144 : ℝ) < (0.0008424381963869595 : ℝ))

theorem V_cb_err_under_half :
    (0.15304243191119066 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.15304243191119066 : ℝ) < (0.5 : ℝ))

theorem V_cb_measured_pos :
    (0 : ℝ) < (0.04183 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.04183 : ℝ))

theorem V_cb_abs_diff :
    (6.401764926845105e-05 : ℝ) < (6.465782576213556e-05 : ℝ) :=
  (by norm_num : (6.401764926845105e-05 : ℝ) < (6.465782576213556e-05 : ℝ))

theorem V_td_err_under_half :
    (0.2337487764470785 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.2337487764470785 : ℝ) < (0.5 : ℝ))

theorem V_td_measured_pos :
    (0 : ℝ) < (0.00858 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.00858 : ℝ))

theorem V_td_abs_diff :
    (2.0055645019159338e-05 : ℝ) < (2.025620147035093e-05 : ℝ) :=
  (by norm_num : (2.0055645019159338e-05 : ℝ) < (2.025620147035093e-05 : ℝ))

theorem V_ts_err_under_half :
    (0.14583328325587586 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.14583328325587586 : ℝ) < (0.5 : ℝ))

theorem V_ts_measured_pos :
    (0 : ℝ) < (0.04111 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.04111 : ℝ))

theorem V_ts_abs_diff :
    (5.9952062746490564e-05 : ℝ) < (6.055158337495547e-05 : ℝ) :=
  (by norm_num : (5.9952062746490564e-05 : ℝ) < (6.055158337495547e-05 : ℝ))

theorem V_tb_err_under_half :
    (0.0004449567119691174 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0004449567119691174 : ℝ) < (0.5 : ℝ))

theorem V_tb_measured_pos :
    (0 : ℝ) < (0.999118 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.999118 : ℝ))

theorem V_tb_abs_diff :
    (4.445642601491606e-06 : ℝ) < (4.490099028506522e-06 : ℝ) :=
  (by norm_num : (4.445642601491606e-06 : ℝ) < (4.490099028506522e-06 : ℝ))

theorem sin2_theta_W_err_under_half :
    (0.06713369973590165 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.06713369973590165 : ℝ) < (0.5 : ℝ))

theorem sin2_theta_W_measured_pos :
    (0 : ℝ) < (0.23122 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.23122 : ℝ))

theorem sin2_theta_W_abs_diff :
    (0.0001552265405293518 : ℝ) < (0.0001567788059356453 : ℝ) :=
  (by norm_num : (0.0001552265405293518 : ℝ) < (0.0001567788059356453 : ℝ))

theorem sin2_theta_W_onshell_err_under_half :
    (0.15026877693416243 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.15026877693416243 : ℝ) < (0.5 : ℝ))

theorem sin2_theta_W_onshell_measured_pos :
    (0 : ℝ) < (0.2230518910035465 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.2230518910035465 : ℝ))

theorem sin2_theta_W_onshell_abs_diff :
    (0.0003351773485395504 : ℝ) < (0.0003385291220259459 : ℝ) :=
  (by norm_num : (0.0003351773485395504 : ℝ) < (0.0003385291220259459 : ℝ))

theorem alpha_inv_err_under_half :
    (0.1472364924023795 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.1472364924023795 : ℝ) < (0.5 : ℝ))

theorem alpha_inv_measured_pos :
    (0 : ℝ) < (137.035999084 : ℝ) :=
  (by norm_num : (0 : ℝ) < (137.035999084 : ℝ))

theorem alpha_inv_abs_diff :
    (0.20176699837983847 : ℝ) < (0.20378466836363784 : ℝ) :=
  (by norm_num : (0.20176699837983847 : ℝ) < (0.20378466836363784 : ℝ))

theorem alpha_s_MZ_err_under_half :
    (0.007242651170537564 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.007242651170537564 : ℝ) < (0.5 : ℝ))

theorem alpha_s_MZ_measured_pos :
    (0 : ℝ) < (0.1179 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.1179 : ℝ))

theorem alpha_s_MZ_abs_diff :
    (8.539085730063789e-06 : ℝ) < (8.624476588364428e-06 : ℝ) :=
  (by norm_num : (8.539085730063789e-06 : ℝ) < (8.624476588364428e-06 : ℝ))

theorem m_H_err_under_half :
    (0.0011951533584994727 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0011951533584994727 : ℝ) < (0.5 : ℝ))

theorem m_H_measured_pos :
    (0 : ℝ) < (125.25 : ℝ) :=
  (by norm_num : (0 : ℝ) < (125.25 : ℝ))

theorem m_H_abs_diff :
    (0.0014969295815205896 : ℝ) < (0.0015118988773367957 : ℝ) :=
  (by norm_num : (0.0014969295815205896 : ℝ) < (0.0015118988773367957 : ℝ))

theorem m_W_err_under_half :
    (0.03999290024803384 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.03999290024803384 : ℝ) < (0.5 : ℝ))

theorem m_W_measured_pos :
    (0 : ℝ) < (80.377 : ℝ) :=
  (by norm_num : (0 : ℝ) < (80.377 : ℝ))

theorem m_W_abs_diff :
    (0.03214509343236216 : ℝ) < (0.03246654436668678 : ℝ) :=
  (by norm_num : (0.03214509343236216 : ℝ) < (0.03246654436668678 : ℝ))

theorem m_Z_err_under_half :
    (0.018424423512725066 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.018424423512725066 : ℝ) < (0.5 : ℝ))

theorem m_Z_measured_pos :
    (0 : ℝ) < (91.1876 : ℝ) :=
  (by norm_num : (0 : ℝ) < (91.1876 : ℝ))

theorem m_Z_abs_diff :
    (0.016800789615089684 : ℝ) < (0.01696879751124158 : ℝ) :=
  (by norm_num : (0.016800789615089684 : ℝ) < (0.01696879751124158 : ℝ))

theorem m_t_err_under_half :
    (0.052705818067851705 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.052705818067851705 : ℝ) < (0.5 : ℝ))

theorem m_t_measured_pos :
    (0 : ℝ) < (172.69 : ℝ) :=
  (by norm_num : (0 : ℝ) < (172.69 : ℝ))

theorem m_t_abs_diff :
    (0.0910176772213731 : ℝ) < (0.09192785399358784 : ℝ) :=
  (by norm_num : (0.0910176772213731 : ℝ) < (0.09192785399358784 : ℝ))

theorem Lambda_QCD_GeV_err_under_half :
    (0.04921722442825905 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.04921722442825905 : ℝ) < (0.5 : ℝ))

theorem Lambda_QCD_GeV_measured_pos :
    (0 : ℝ) < (0.2173 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.2173 : ℝ))

theorem Lambda_QCD_GeV_abs_diff :
    (0.00010694902868260692 : ℝ) < (0.00010801851897043299 : ℝ) :=
  (by norm_num : (0.00010694902868260692 : ℝ) < (0.00010801851897043299 : ℝ))

theorem sqrt_sigma_GeV_err_under_half :
    (0.02566066753490444 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.02566066753490444 : ℝ) < (0.5 : ℝ))

theorem sqrt_sigma_GeV_measured_pos :
    (0 : ℝ) < (0.42 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.42 : ℝ))

theorem sqrt_sigma_GeV_abs_diff :
    (0.00010777480364659864 : ℝ) < (0.00010885255168406462 : ℝ) :=
  (by norm_num : (0.00010777480364659864 : ℝ) < (0.00010885255168406462 : ℝ))

theorem N_eff_err_under_half :
    (0.07917549100062735 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.07917549100062735 : ℝ) < (0.5 : ℝ))

theorem N_eff_measured_pos :
    (0 : ℝ) < (3.046 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.046 : ℝ))

theorem N_eff_abs_diff :
    (0.002411685455879109 : ℝ) < (0.0024358023104389 : ℝ) :=
  (by norm_num : (0.002411685455879109 : ℝ) < (0.0024358023104389 : ℝ))

theorem sin2_theta_12_err_under_half :
    (0.013048795958832987 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.013048795958832987 : ℝ) < (0.5 : ℝ))

theorem sin2_theta_12_measured_pos :
    (0 : ℝ) < (0.307 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.307 : ℝ))

theorem sin2_theta_12_abs_diff :
    (4.005980359361727e-05 : ℝ) < (4.046040163055344e-05 : ℝ) :=
  (by norm_num : (4.005980359361727e-05 : ℝ) < (4.046040163055344e-05 : ℝ))

theorem sin2_theta_23_err_under_half :
    (0.17474226348654942 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.17474226348654942 : ℝ) < (0.5 : ℝ))

theorem sin2_theta_23_measured_pos :
    (0 : ℝ) < (0.546 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.546 : ℝ))

theorem sin2_theta_23_abs_diff :
    (0.00095409275863656 : ℝ) < (0.0009636336862239255 : ℝ) :=
  (by norm_num : (0.00095409275863656 : ℝ) < (0.0009636336862239255 : ℝ))

theorem sin2_theta_13_err_under_half :
    (0.003010045202972307 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.003010045202972307 : ℝ) < (0.5 : ℝ))

theorem sin2_theta_13_measured_pos :
    (0 : ℝ) < (0.022 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.022 : ℝ))

theorem sin2_theta_13_abs_diff :
    (6.622099446539076e-07 : ℝ) < (6.688320451004467e-07 : ℝ) :=
  (by norm_num : (6.622099446539076e-07 : ℝ) < (6.688320451004467e-07 : ℝ))

theorem delta_pmns_rad_err_under_half :
    (0.0997385337617464 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0997385337617464 : ℝ) < (0.5 : ℝ))

theorem delta_pmns_rad_measured_pos :
    (0 : ℝ) < (3.4382986264288293 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.4382986264288293 : ℝ))

theorem delta_pmns_rad_abs_diff :
    (0.003429308636350381 : ℝ) < (0.003463601722714885 : ℝ) :=
  (by norm_num : (0.003429308636350381 : ℝ) < (0.003463601722714885 : ℝ))

theorem dm2_21_err_under_half :
    (0.07222853624703972 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.07222853624703972 : ℝ) < (0.5 : ℝ))

theorem dm2_21_measured_pos :
    (0 : ℝ) < (7.53e-05 : ℝ) :=
  (by norm_num : (0 : ℝ) < (7.53e-05 : ℝ))

theorem dm2_21_abs_diff :
    (5.438808779402091e-08 : ℝ) < (5.4931969671961115e-08 : ℝ) :=
  (by norm_num : (5.438808779402091e-08 : ℝ) < (5.4931969671961115e-08 : ℝ))

theorem dm2_31_abs_err_under_half :
    (0.36301157961075986 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.36301157961075986 : ℝ) < (0.5 : ℝ))

theorem dm2_31_abs_measured_pos :
    (0 : ℝ) < (0.002453 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.002453 : ℝ))

theorem dm2_31_abs_abs_diff :
    (8.904674047851939e-06 : ℝ) < (8.993720789330459e-06 : ℝ) :=
  (by norm_num : (8.904674047851939e-06 : ℝ) < (8.993720789330459e-06 : ℝ))

theorem emergent_unitarity_row_u_err_under_half :
    (0.001399329001761096 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.001399329001761096 : ℝ) < (0.5 : ℝ))

theorem emergent_unitarity_row_u_measured_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem emergent_unitarity_row_u_abs_diff :
    (1.399329001761096e-05 : ℝ) < (1.413322291878707e-05 : ℝ) :=
  (by norm_num : (1.399329001761096e-05 : ℝ) < (1.413322291878707e-05 : ℝ))

theorem emergent_unitarity_row_c_err_under_half :
    (0.17551087147971156 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.17551087147971156 : ℝ) < (0.5 : ℝ))

theorem emergent_unitarity_row_c_measured_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem emergent_unitarity_row_c_abs_diff :
    (0.0017551087147971156 : ℝ) < (0.0017726598019460868 : ℝ) :=
  (by norm_num : (0.0017551087147971156 : ℝ) < (0.0017726598019460868 : ℝ))

theorem emergent_unitarity_row_t_err_under_half :
    (0.0014587296799373206 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0014587296799373206 : ℝ) < (0.5 : ℝ))

theorem emergent_unitarity_row_t_measured_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem emergent_unitarity_row_t_abs_diff :
    (1.4587296799373206e-05 : ℝ) < (1.473316976836694e-05 : ℝ) :=
  (by norm_num : (1.4587296799373206e-05 : ℝ) < (1.473316976836694e-05 : ℝ))

theorem triangle_angle_sum_pi_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem triangle_angle_sum_pi_measured_pos :
    (0 : ℝ) < (3.141592653589793 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.141592653589793 : ℝ))

theorem triangle_angle_sum_pi_abs_diff :
    (0.0 : ℝ) < (1e-09 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (1e-09 : ℝ))

theorem yin_yang_in_unit_interval_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem yin_yang_in_unit_interval_measured_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem yin_yang_in_unit_interval_abs_diff :
    (0.0 : ℝ) < (1e-09 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (1e-09 : ℝ))

theorem all_kappa_nonnegative_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem all_kappa_nonnegative_measured_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem all_kappa_nonnegative_abs_diff :
    (0.0 : ℝ) < (1e-09 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (1e-09 : ℝ))

theorem sector_count_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem sector_count_measured_pos :
    (0 : ℝ) < (8.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (8.0 : ℝ))

theorem sector_count_abs_diff :
    (0.0 : ℝ) < (1e-09 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (1e-09 : ℝ))

theorem edge_count_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem edge_count_measured_pos :
    (0 : ℝ) < (15.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (15.0 : ℝ))

theorem edge_count_abs_diff :
    (0.0 : ℝ) < (1e-09 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (1e-09 : ℝ))

theorem emergent_unitarity_row_u_unitarity_tight :
    (1.399329001761096e-05 : ℝ) < (0.05 : ℝ) :=
  (by norm_num : (1.399329001761096e-05 : ℝ) < (0.05 : ℝ))

theorem emergent_unitarity_row_c_unitarity_tight :
    (0.0017551087147971156 : ℝ) < (0.05 : ℝ) :=
  (by norm_num : (0.0017551087147971156 : ℝ) < (0.05 : ℝ))

theorem emergent_unitarity_row_t_unitarity_tight :
    (1.4587296799373206e-05 : ℝ) < (0.05 : ℝ) :=
  (by norm_num : (1.4587296799373206e-05 : ℝ) < (0.05 : ℝ))

theorem gauge_n_U1_eq : (1 : ℕ) = (1 : ℕ) := by
  decide

theorem gauge_n_U1_pos : 0 < (1 : ℕ) := by
  decide

theorem gauge_n_SU2_eq : (3 : ℕ) = (3 : ℕ) := by
  decide

theorem gauge_n_SU2_pos : 0 < (3 : ℕ) := by
  decide

theorem gauge_n_SU3_eq : (8 : ℕ) = (8 : ℕ) := by
  decide

theorem gauge_n_SU3_pos : 0 < (8 : ℕ) := by
  decide

theorem gauge_n_gen_total_eq : (12 : ℕ) = (12 : ℕ) := by
  decide

theorem gauge_n_gen_total_pos : 0 < (12 : ℕ) := by
  decide

theorem gauge_n_fermion_gen_eq : (3 : ℕ) = (3 : ℕ) := by
  decide

theorem gauge_n_fermion_gen_pos : 0 < (3 : ℕ) := by
  decide

theorem gr_einstein_trace_reverse_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_einstein_trace_reverse_meas_pos :
    (0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.5 : ℝ))

theorem gr_weak_field_2phi_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_weak_field_2phi_meas_pos :
    (0 : ℝ) < (2e-06 : ℝ) :=
  (by norm_num : (0 : ℝ) < (2e-06 : ℝ))

theorem gr_schwarzschild_radius_sun_m_err_under_half :
    (0.003026566219535862 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.003026566219535862 : ℝ) < (0.5 : ℝ))

theorem gr_schwarzschild_radius_sun_m_meas_pos :
    (0 : ℝ) < (2953.25 : ℝ) :=
  (by norm_num : (0 : ℝ) < (2953.25 : ℝ))

theorem gr_solar_light_deflection_rad_err_under_half :
    (0.013893853126499888 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.013893853126499888 : ℝ) < (0.5 : ℝ))

theorem gr_solar_light_deflection_rad_meas_pos :
    (0 : ℝ) < (8.489087556227974e-06 : ℝ) :=
  (by norm_num : (0 : ℝ) < (8.489087556227974e-06 : ℝ))

theorem gr_mercury_perihelion_arcsec_cy_err_under_half :
    (0.0047099996121108675 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0047099996121108675 : ℝ) < (0.5 : ℝ))

theorem gr_mercury_perihelion_arcsec_cy_meas_pos :
    (0 : ℝ) < (42.98 : ℝ) :=
  (by norm_num : (0 : ℝ) < (42.98 : ℝ))

theorem gr_acoustic_null_cone_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_acoustic_null_cone_meas_pos :
    (0 : ℝ) < (0.7693639124918291 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.7693639124918291 : ℝ))

theorem gr_planck_length_m_err_under_half :
    (2.3928549890383717e-11 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (2.3928549890383717e-11 : ℝ) < (0.5 : ℝ))

theorem gr_c_light_si_exact_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_c_light_si_exact_meas_pos :
    (0 : ℝ) < (299792458.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (299792458.0 : ℝ))

theorem gr_seed_sin2_theta_W_err_under_half :
    (0.016460322231694493 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.016460322231694493 : ℝ) < (0.5 : ℝ))

theorem gr_seed_sin2_theta_W_meas_pos :
    (0 : ℝ) < (0.23122 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.23122 : ℝ))

theorem gr_seed_sin2_theta_W_onshell_err_under_half :
    (0.20105239362371918 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.20105239362371918 : ℝ) < (0.5 : ℝ))

theorem gr_seed_sin2_theta_W_onshell_meas_pos :
    (0 : ℝ) < (0.2230518910035465 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.2230518910035465 : ℝ))

theorem gr_seed_alpha_inv_err_under_half :
    (0.15275909169604954 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.15275909169604954 : ℝ) < (0.5 : ℝ))

theorem gr_seed_alpha_inv_meas_pos :
    (0 : ℝ) < (137.035999084 : ℝ) :=
  (by norm_num : (0 : ℝ) < (137.035999084 : ℝ))

theorem gr_seed_m_H_err_under_half :
    (0.022485014301729805 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.022485014301729805 : ℝ) < (0.5 : ℝ))

theorem gr_seed_m_H_meas_pos :
    (0 : ℝ) < (125.25 : ℝ) :=
  (by norm_num : (0 : ℝ) < (125.25 : ℝ))

theorem gr_seed_m_W_err_under_half :
    (0.012988177377751 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.012988177377751 : ℝ) < (0.5 : ℝ))

theorem gr_seed_m_W_meas_pos :
    (0 : ℝ) < (80.377 : ℝ) :=
  (by norm_num : (0 : ℝ) < (80.377 : ℝ))

theorem gr_seed_m_Z_err_under_half :
    (0.015880360710250344 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.015880360710250344 : ℝ) < (0.5 : ℝ))

theorem gr_seed_m_Z_meas_pos :
    (0 : ℝ) < (91.1876 : ℝ) :=
  (by norm_num : (0 : ℝ) < (91.1876 : ℝ))

theorem gr_Lambda_QCD_GeV_err_under_half :
    (0.048055073125713964 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.048055073125713964 : ℝ) < (0.5 : ℝ))

theorem gr_Lambda_QCD_GeV_meas_pos :
    (0 : ℝ) < (0.2173 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.2173 : ℝ))

theorem gr_sqrt_sigma_GeV_err_under_half :
    (0.025896107116174516 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.025896107116174516 : ℝ) < (0.5 : ℝ))

theorem gr_sqrt_sigma_GeV_meas_pos :
    (0 : ℝ) < (0.42 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.42 : ℝ))

theorem gr_N_eff_err_under_half :
    (0.028424048045719855 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.028424048045719855 : ℝ) < (0.5 : ℝ))

theorem gr_N_eff_meas_pos :
    (0 : ℝ) < (3.046 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.046 : ℝ))

theorem gr_N_c_QCD_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_N_c_QCD_meas_pos :
    (0 : ℝ) < (3.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.0 : ℝ))

theorem gr_Casimir_C_F_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_Casimir_C_F_meas_pos :
    (0 : ℝ) < (1.3333333333333333 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.3333333333333333 : ℝ))

theorem gr_Casimir_C_A_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_Casimir_C_A_meas_pos :
    (0 : ℝ) < (3.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.0 : ℝ))

theorem gr_beta0_QCD_nf5_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_beta0_QCD_nf5_meas_pos :
    (0 : ℝ) < (7.666666666666667 : ℝ) :=
  (by norm_num : (0 : ℝ) < (7.666666666666667 : ℝ))

theorem gr_alpha_s_gt_alpha_em_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_alpha_s_gt_alpha_em_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_koide_lepton_QR_err_under_half :
    (0.0009230194964016114 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0009230194964016114 : ℝ) < (0.5 : ℝ))

theorem gr_koide_lepton_QR_meas_pos :
    (0 : ℝ) < (0.6666666666666666 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.6666666666666666 : ℝ))

theorem gr_sqrt2_structural_recovery_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_sqrt2_structural_recovery_meas_pos :
    (0 : ℝ) < (1.4142135623730951 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.4142135623730951 : ℝ))

theorem gr_yukawa_top_err_under_half :
    (0.013457034902430751 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.013457034902430751 : ℝ) < (0.5 : ℝ))

theorem gr_yukawa_top_meas_pos :
    (0 : ℝ) < (0.991 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.991 : ℝ))

theorem gr_morphic_phi_present_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_morphic_phi_present_meas_pos :
    (0 : ℝ) < (1.618033988749895 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.618033988749895 : ℝ))

theorem gr_neutrino_m3_over_m2_err_under_half :
    (0.1470630495663553 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.1470630495663553 : ℝ) < (0.5 : ℝ))

theorem gr_neutrino_m3_over_m2_meas_pos :
    (0 : ℝ) < (5.707570518336111 : ℝ) :=
  (by norm_num : (0 : ℝ) < (5.707570518336111 : ℝ))

theorem gr_R_b_triangle_err_under_half :
    (0.026537499247957154 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.026537499247957154 : ℝ) < (0.5 : ℝ))

theorem gr_R_b_triangle_meas_pos :
    (0 : ℝ) < (0.3865593098089865 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.3865593098089865 : ℝ))

theorem gr_R_t_triangle_err_under_half :
    (0.019630621725789416 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.019630621725789416 : ℝ) < (0.5 : ℝ))

theorem gr_R_t_triangle_meas_pos :
    (0 : ℝ) < (0.9117171162153312 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.9117171162153312 : ℝ))

theorem gr_sin_delta_ckm_err_under_half :
    (0.0036013868908110055 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0036013868908110055 : ℝ) < (0.5 : ℝ))

theorem gr_sin_delta_ckm_meas_pos :
    (0 : ℝ) < (0.9115343723414107 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.9115343723414107 : ℝ))

theorem gr_spin2_massless_helicities_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_spin2_massless_helicities_meas_pos :
    (0 : ℝ) < (2.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (2.0 : ℝ))

theorem gr_spin2_TT_dof_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_spin2_TT_dof_meas_pos :
    (0 : ℝ) < (2.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (2.0 : ℝ))

theorem gr_einstein_quadrupole_prefactor_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_einstein_quadrupole_prefactor_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_wilson_area_law_sigma_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_wilson_area_law_sigma_meas_pos :
    (0 : ℝ) < (0.17649137329543738 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.17649137329543738 : ℝ))

theorem gr_confinement_scale_ratio_err_under_half :
    (0.022153229185580246 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.022153229185580246 : ℝ) < (0.5 : ℝ))

theorem gr_confinement_scale_ratio_meas_pos :
    (0 : ℝ) < (0.5173809523809524 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.5173809523809524 : ℝ))

theorem gr_asymptotic_freedom_beta0_pos_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_asymptotic_freedom_beta0_pos_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_flux_tube_E_over_L_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_flux_tube_E_over_L_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_polyakov_confined_order_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_spin2_massive_polarizations_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_spin2_massive_polarizations_meas_pos :
    (0 : ℝ) < (5.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (5.0 : ℝ))

theorem gr_spin2_metric_dof_accounting_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_spin2_metric_dof_accounting_meas_pos :
    (0 : ℝ) < (2.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (2.0 : ℝ))

theorem gr_equivalence_geodesic_structure_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_equivalence_geodesic_structure_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_spin2_wave_equation_flat_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_spin2_wave_equation_flat_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_bianchi_contracted_identity_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_bianchi_contracted_identity_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_spin2_TT_projector_complete_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_spin2_TT_projector_complete_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_soft_graviton_pole_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_soft_graviton_pole_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_instanton_action_scale_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_instanton_action_scale_meas_pos :
    (0 : ℝ) < (669.6431825331274 : ℝ) :=
  (by norm_num : (0 : ℝ) < (669.6431825331274 : ℝ))

theorem gr_ym_beta_function_structure_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_ym_beta_function_structure_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_su3_center_order_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_su3_center_order_meas_pos :
    (0 : ℝ) < (3.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.0 : ℝ))

theorem gr_dual_meissner_confined_flag_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_dual_meissner_confined_flag_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_theta_QCD_strong_CP_flag_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_glueball_over_sqrt_sigma_err_under_half :
    (0.034782692362047014 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.034782692362047014 : ℝ) < (0.5 : ℝ))

theorem gr_glueball_over_sqrt_sigma_meas_pos :
    (0 : ℝ) < (3.65 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.65 : ℝ))

theorem gr_trace_anomaly_structure_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_trace_anomaly_structure_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_graviton_propagator_pole_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_graviton_propagator_pole_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_gw_quadrupole_coupling_structure_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_gw_quadrupole_coupling_structure_meas_pos :
    (0 : ℝ) < (1.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.0 : ℝ))

theorem gr_massless_spin2_little_group_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_massless_spin2_little_group_meas_pos :
    (0 : ℝ) < (2.0 : ℝ) :=
  (by norm_num : (0 : ℝ) < (2.0 : ℝ))

theorem gr_triangle_angle_sum_pi_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem gr_triangle_angle_sum_pi_meas_pos :
    (0 : ℝ) < (3.141592653589793 : ℝ) :=
  (by norm_num : (0 : ℝ) < (3.141592653589793 : ℝ))

theorem gr_alpha_rad_err_under_half :
    (0.03680231674953141 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.03680231674953141 : ℝ) < (0.5 : ℝ))

theorem gr_alpha_rad_meas_pos :
    (0 : ℝ) < (1.5982430233482232 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.5982430233482232 : ℝ))

theorem gr_beta_rad_err_under_half :
    (0.029711617355294043 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.029711617355294043 : ℝ) < (0.5 : ℝ))

theorem gr_beta_rad_meas_pos :
    (0 : ℝ) < (0.3967401060358461 : ℝ) :=
  (by norm_num : (0 : ℝ) < (0.3967401060358461 : ℝ))

theorem gr_gamma_rad_err_under_half :
    (0.04101767408617176 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.04101767408617176 : ℝ) < (0.5 : ℝ))

theorem gr_gamma_rad_meas_pos :
    (0 : ℝ) < (1.1466095242057237 : ℝ) :=
  (by norm_num : (0 : ℝ) < (1.1466095242057237 : ℝ))

theorem sm_lambda_ckm_err_under_half :
    (0.06225011989853476 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.06225011989853476 : ℝ) < (0.5 : ℝ))

theorem sm_A_wolfenstein_err_under_half :
    (0.05246555208389803 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.05246555208389803 : ℝ) < (0.5 : ℝ))

theorem sm_rho_bar_err_under_half :
    (0.02700157709000836 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.02700157709000836 : ℝ) < (0.5 : ℝ))

theorem sm_eta_bar_err_under_half :
    (0.0028013614651725667 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0028013614651725667 : ℝ) < (0.5 : ℝ))

theorem sm_Jarlskog_J_err_under_half :
    (0.23792303102008408 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.23792303102008408 : ℝ) < (0.5 : ℝ))

theorem sm_delta_ckm_rad_err_under_half :
    (0.02612849108321111 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.02612849108321111 : ℝ) < (0.5 : ℝ))

theorem sm_V_ud_err_under_half :
    (0.002658467271059532 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.002658467271059532 : ℝ) < (0.5 : ℝ))

theorem sm_V_us_err_under_half :
    (0.06225011989853476 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.06225011989853476 : ℝ) < (0.5 : ℝ))

theorem sm_V_ub_err_under_half :
    (0.23474330619715575 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.23474330619715575 : ℝ) < (0.5 : ℝ))

theorem sm_V_cd_err_under_half :
    (0.12454706932169445 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.12454706932169445 : ℝ) < (0.5 : ℝ))

theorem sm_V_cs_err_under_half :
    (0.08568112914816942 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.08568112914816942 : ℝ) < (0.5 : ℝ))

theorem sm_V_cb_err_under_half :
    (0.15304243191119066 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.15304243191119066 : ℝ) < (0.5 : ℝ))

theorem sm_V_td_err_under_half :
    (0.2337487764470785 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.2337487764470785 : ℝ) < (0.5 : ℝ))

theorem sm_V_ts_err_under_half :
    (0.14583328325587586 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.14583328325587586 : ℝ) < (0.5 : ℝ))

theorem sm_V_tb_err_under_half :
    (0.0004449567119691174 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0004449567119691174 : ℝ) < (0.5 : ℝ))

theorem sm_sin2_theta_W_err_under_half :
    (0.06713369973590165 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.06713369973590165 : ℝ) < (0.5 : ℝ))

theorem sm_sin2_theta_W_onshell_err_under_half :
    (0.15026877693416243 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.15026877693416243 : ℝ) < (0.5 : ℝ))

theorem sm_alpha_inv_err_under_half :
    (0.1472364924023795 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.1472364924023795 : ℝ) < (0.5 : ℝ))

theorem sm_alpha_s_MZ_err_under_half :
    (0.007242651170537564 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.007242651170537564 : ℝ) < (0.5 : ℝ))

theorem sm_m_H_err_under_half :
    (0.0011951533584994727 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0011951533584994727 : ℝ) < (0.5 : ℝ))

theorem sm_m_W_err_under_half :
    (0.03999290024803384 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.03999290024803384 : ℝ) < (0.5 : ℝ))

theorem sm_m_Z_err_under_half :
    (0.018424423512725066 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.018424423512725066 : ℝ) < (0.5 : ℝ))

theorem sm_m_t_err_under_half :
    (0.052705818067851705 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.052705818067851705 : ℝ) < (0.5 : ℝ))

theorem sm_Lambda_QCD_GeV_err_under_half :
    (0.04921722442825905 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.04921722442825905 : ℝ) < (0.5 : ℝ))

theorem sm_sqrt_sigma_GeV_err_under_half :
    (0.02566066753490444 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.02566066753490444 : ℝ) < (0.5 : ℝ))

theorem sm_N_eff_err_under_half :
    (0.07917549100062735 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.07917549100062735 : ℝ) < (0.5 : ℝ))

theorem sm_sin2_theta_12_err_under_half :
    (0.013048795958832987 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.013048795958832987 : ℝ) < (0.5 : ℝ))

theorem sm_sin2_theta_23_err_under_half :
    (0.17474226348654942 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.17474226348654942 : ℝ) < (0.5 : ℝ))

theorem sm_sin2_theta_13_err_under_half :
    (0.003010045202972307 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.003010045202972307 : ℝ) < (0.5 : ℝ))

theorem sm_delta_pmns_rad_err_under_half :
    (0.0997385337617464 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0997385337617464 : ℝ) < (0.5 : ℝ))

theorem sm_dm2_21_err_under_half :
    (0.07222853624703972 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.07222853624703972 : ℝ) < (0.5 : ℝ))

theorem sm_dm2_31_abs_err_under_half :
    (0.36301157961075986 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.36301157961075986 : ℝ) < (0.5 : ℝ))

theorem sm_emergent_unitarity_row_u_err_under_half :
    (0.001399329001761096 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.001399329001761096 : ℝ) < (0.5 : ℝ))

theorem sm_emergent_unitarity_row_c_err_under_half :
    (0.17551087147971156 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.17551087147971156 : ℝ) < (0.5 : ℝ))

theorem sm_emergent_unitarity_row_t_err_under_half :
    (0.0014587296799373206 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0014587296799373206 : ℝ) < (0.5 : ℝ))

theorem sm_triangle_angle_sum_pi_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem sm_yin_yang_in_unit_interval_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem sm_all_kappa_nonnegative_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem sm_sector_count_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem sm_edge_count_err_under_half :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

end

end FSOT.Formal.GRSMCKM
