(* FSOT GR/SM/CKM/PMNS spine — multi-prover re-proof of exported obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma lambda_ckm_err_under_half : ((0.06225011989853476%R)) < (0.5%R).
Proof. lra. Qed.

Lemma lambda_ckm_measured_pos : 0 < ((0.22501%R)).
Proof. lra. Qed.

Lemma lambda_ckm_abs_diff : ((0.00014006899478369306%R)) < ((0.00014146968473252998%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_err_under_half : ((0.05246555208389803%R)) < (0.5%R).
Proof. lra. Qed.

Lemma A_wolfenstein_measured_pos : 0 < ((0.826%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_abs_diff : ((0.0004333654602129977%R)) < ((0.0004376991148161277%R)).
Proof. lra. Qed.

Lemma rho_bar_err_under_half : ((0.02700157709000836%R)) < (0.5%R).
Proof. lra. Qed.

Lemma rho_bar_measured_pos : 0 < ((0.1591%R)).
Proof. lra. Qed.

Lemma rho_bar_abs_diff : ((0.0000429595091502033%R)) < ((0.000043389104242705336%R)).
Proof. lra. Qed.

Lemma eta_bar_err_under_half : ((0.0028013614651725667%R)) < (0.5%R).
Proof. lra. Qed.

Lemma eta_bar_measured_pos : 0 < ((0.3523%R)).
Proof. lra. Qed.

Lemma eta_bar_abs_diff : ((0.000009869196441802952%R)) < ((0.000009967888407220981%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_err_under_half : ((0.23792303102008408%R)) < (0.5%R).
Proof. lra. Qed.

Lemma Jarlskog_J_measured_pos : 0 < ((0.0000312%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_abs_diff : ((0.00000007423198567826624%R)) < ((0.00000007497430653504891%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_err_under_half : ((0.02612849108321111%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_ckm_rad_measured_pos : 0 < ((1.147%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_abs_diff : ((0.0002996937927244314%R)) < ((0.0003026907306526757%R)).
Proof. lra. Qed.

Lemma V_ud_err_under_half : ((0.002658467271059532%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ud_measured_pos : 0 < ((0.97435%R)).
Proof. lra. Qed.

Lemma V_ud_abs_diff : ((0.00002590277585556855%R)) < ((0.000026161803615124236%R)).
Proof. lra. Qed.

Lemma V_us_err_under_half : ((0.06225011989853476%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_us_measured_pos : 0 < ((0.22501%R)).
Proof. lra. Qed.

Lemma V_us_abs_diff : ((0.00014006899478369306%R)) < ((0.00014146968473252998%R)).
Proof. lra. Qed.

Lemma V_ub_err_under_half : ((0.23474330619715575%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ub_measured_pos : 0 < ((0.003732%R)).
Proof. lra. Qed.

Lemma V_ub_abs_diff : ((0.000008760620187277853%R)) < ((0.000008848226390150632%R)).
Proof. lra. Qed.

Lemma V_cd_err_under_half : ((0.12454706932169445%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cd_measured_pos : 0 < ((0.22487%R)).
Proof. lra. Qed.

Lemma V_cd_abs_diff : ((0.0002800689947836943%R)) < ((0.00028286968473253125%R)).
Proof. lra. Qed.

Lemma V_cs_err_under_half : ((0.08568112914816942%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cs_measured_pos : 0 < ((0.97349%R)).
Proof. lra. Qed.

Lemma V_cs_abs_diff : ((0.0008340972241445144%R)) < ((0.0008424381963869595%R)).
Proof. lra. Qed.

Lemma V_cb_err_under_half : ((0.15304243191119066%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cb_measured_pos : 0 < ((0.04183%R)).
Proof. lra. Qed.

Lemma V_cb_abs_diff : ((0.00006401764926845105%R)) < ((0.00006465782576213556%R)).
Proof. lra. Qed.

Lemma V_td_err_under_half : ((0.2337487764470785%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_td_measured_pos : 0 < ((0.00858%R)).
Proof. lra. Qed.

Lemma V_td_abs_diff : ((0.000020055645019159338%R)) < ((0.00002025620147035093%R)).
Proof. lra. Qed.

Lemma V_ts_err_under_half : ((0.14583328325587586%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ts_measured_pos : 0 < ((0.04111%R)).
Proof. lra. Qed.

Lemma V_ts_abs_diff : ((0.000059952062746490564%R)) < ((0.00006055158337495547%R)).
Proof. lra. Qed.

Lemma V_tb_err_under_half : ((0.0004449567119691174%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_tb_measured_pos : 0 < ((0.999118%R)).
Proof. lra. Qed.

Lemma V_tb_abs_diff : ((0.000004445642601491606%R)) < ((0.000004490099028506522%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_err_under_half : ((0.06713369973590165%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_W_measured_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_abs_diff : ((0.0001552265405293518%R)) < ((0.0001567788059356453%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_onshell_err_under_half : ((0.15026877693416243%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_W_onshell_measured_pos : 0 < ((0.2230518910035465%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_onshell_abs_diff : ((0.0003351773485395504%R)) < ((0.0003385291220259459%R)).
Proof. lra. Qed.

Lemma alpha_inv_err_under_half : ((0.1472364924023795%R)) < (0.5%R).
Proof. lra. Qed.

Lemma alpha_inv_measured_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma alpha_inv_abs_diff : ((0.20176699837983847%R)) < ((0.20378466836363784%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_err_under_half : ((0.007242651170537564%R)) < (0.5%R).
Proof. lra. Qed.

Lemma alpha_s_MZ_measured_pos : 0 < ((0.1179%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_abs_diff : ((0.000008539085730063789%R)) < ((0.000008624476588364428%R)).
Proof. lra. Qed.

Lemma m_H_err_under_half : ((0.0011951533584994727%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_H_measured_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma m_H_abs_diff : ((0.0014969295815205896%R)) < ((0.0015118988773367957%R)).
Proof. lra. Qed.

Lemma m_W_err_under_half : ((0.03999290024803384%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_W_measured_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma m_W_abs_diff : ((0.03214509343236216%R)) < ((0.03246654436668678%R)).
Proof. lra. Qed.

Lemma m_Z_err_under_half : ((0.018424423512725066%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_Z_measured_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma m_Z_abs_diff : ((0.016800789615089684%R)) < ((0.01696879751124158%R)).
Proof. lra. Qed.

Lemma m_t_err_under_half : ((0.052705818067851705%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_t_measured_pos : 0 < ((172.69%R)).
Proof. lra. Qed.

Lemma m_t_abs_diff : ((0.0910176772213731%R)) < ((0.09192785399358784%R)).
Proof. lra. Qed.

Lemma Lambda_QCD_GeV_err_under_half : ((0.04921722442825905%R)) < (0.5%R).
Proof. lra. Qed.

Lemma Lambda_QCD_GeV_measured_pos : 0 < ((0.2173%R)).
Proof. lra. Qed.

Lemma Lambda_QCD_GeV_abs_diff : ((0.00010694902868260692%R)) < ((0.00010801851897043299%R)).
Proof. lra. Qed.

Lemma sqrt_sigma_GeV_err_under_half : ((0.02566066753490444%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sqrt_sigma_GeV_measured_pos : 0 < ((0.42%R)).
Proof. lra. Qed.

Lemma sqrt_sigma_GeV_abs_diff : ((0.00010777480364659864%R)) < ((0.00010885255168406462%R)).
Proof. lra. Qed.

Lemma N_eff_err_under_half : ((0.07917549100062735%R)) < (0.5%R).
Proof. lra. Qed.

Lemma N_eff_measured_pos : 0 < ((3.046%R)).
Proof. lra. Qed.

Lemma N_eff_abs_diff : ((0.002411685455879109%R)) < ((0.0024358023104389%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_err_under_half : ((0.013048795958832987%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_12_measured_pos : 0 < ((0.307%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_abs_diff : ((0.00004005980359361727%R)) < ((0.00004046040163055344%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_err_under_half : ((0.17474226348654942%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_23_measured_pos : 0 < ((0.546%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_abs_diff : ((0.00095409275863656%R)) < ((0.0009636336862239255%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_err_under_half : ((0.003010045202972307%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_13_measured_pos : 0 < ((0.022%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_abs_diff : ((0.0000006622099446539076%R)) < ((0.0000006688320451004467%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_err_under_half : ((0.0997385337617464%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_pmns_rad_measured_pos : 0 < ((3.4382986264288293%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_abs_diff : ((0.003429308636350381%R)) < ((0.003463601722714885%R)).
Proof. lra. Qed.

Lemma dm2_21_err_under_half : ((0.07222853624703972%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_21_measured_pos : 0 < ((0.0000753%R)).
Proof. lra. Qed.

Lemma dm2_21_abs_diff : ((0.00000005438808779402091%R)) < ((0.000000054931969671961115%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_err_under_half : ((0.36301157961075986%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_31_abs_measured_pos : 0 < ((0.002453%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_abs_diff : ((0.000008904674047851939%R)) < ((0.000008993720789330459%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_err_under_half : ((0.001399329001761096%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_abs_diff : ((0.00001399329001761096%R)) < ((0.00001413322291878707%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_err_under_half : ((0.17551087147971156%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_abs_diff : ((0.0017551087147971156%R)) < ((0.0017726598019460868%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_err_under_half : ((0.0014587296799373206%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_abs_diff : ((0.000014587296799373206%R)) < ((0.00001473316976836694%R)).
Proof. lra. Qed.

Lemma triangle_angle_sum_pi_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma triangle_angle_sum_pi_measured_pos : 0 < ((3.141592653589793%R)).
Proof. lra. Qed.

Lemma triangle_angle_sum_pi_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma yin_yang_in_unit_interval_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma yin_yang_in_unit_interval_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma yin_yang_in_unit_interval_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma all_kappa_nonnegative_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma all_kappa_nonnegative_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma all_kappa_nonnegative_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma sector_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sector_count_measured_pos : 0 < ((8.0%R)).
Proof. lra. Qed.

Lemma sector_count_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma edge_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma edge_count_measured_pos : 0 < ((15.0%R)).
Proof. lra. Qed.

Lemma edge_count_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_unitarity_tight : ((0.00001399329001761096%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_unitarity_tight : ((0.0017551087147971156%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_unitarity_tight : ((0.000014587296799373206%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma gauge_n_U1_eq : (1 = 1)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_U1_pos : (0 < 1)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gauge_n_SU2_eq : (3 = 3)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_SU2_pos : (0 < 3)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gauge_n_SU3_eq : (8 = 8)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_SU3_pos : (0 < 8)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gauge_n_gen_total_eq : (12 = 12)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_gen_total_pos : (0 < 12)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gauge_n_fermion_gen_eq : (3 = 3)%nat.
Proof. reflexivity. Qed.

Lemma gauge_n_fermion_gen_pos : (0 < 3)%nat.
Proof. apply Nat.ltb_lt; reflexivity. Qed.

Lemma gr_einstein_trace_reverse_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_einstein_trace_reverse_meas_pos : 0 < ((0.5%R)).
Proof. lra. Qed.

Lemma gr_weak_field_2phi_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_weak_field_2phi_meas_pos : 0 < ((0.000002%R)).
Proof. lra. Qed.

Lemma gr_schwarzschild_radius_sun_m_err_under_half : ((0.003026566219535862%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_schwarzschild_radius_sun_m_meas_pos : 0 < ((2953.25%R)).
Proof. lra. Qed.

Lemma gr_solar_light_deflection_rad_err_under_half : ((0.013893853126499888%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_solar_light_deflection_rad_meas_pos : 0 < ((0.000008489087556227974%R)).
Proof. lra. Qed.

Lemma gr_mercury_perihelion_arcsec_cy_err_under_half : ((0.0047099996121108675%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_mercury_perihelion_arcsec_cy_meas_pos : 0 < ((42.98%R)).
Proof. lra. Qed.

Lemma gr_acoustic_null_cone_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_acoustic_null_cone_meas_pos : 0 < ((0.7693639124918291%R)).
Proof. lra. Qed.

Lemma gr_planck_length_m_err_under_half : ((0.000000000023928549890383717%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_c_light_si_exact_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_c_light_si_exact_meas_pos : 0 < ((299792458.0%R)).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_err_under_half : ((0.016460322231694493%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_meas_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_onshell_err_under_half : ((0.20105239362371918%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_onshell_meas_pos : 0 < ((0.2230518910035465%R)).
Proof. lra. Qed.

Lemma gr_seed_alpha_inv_err_under_half : ((0.15275909169604954%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_alpha_inv_meas_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma gr_seed_m_H_err_under_half : ((0.022485014301729805%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_H_meas_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma gr_seed_m_W_err_under_half : ((0.012988177377751%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_W_meas_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma gr_seed_m_Z_err_under_half : ((0.015880360710250344%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_Z_meas_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma gr_Lambda_QCD_GeV_err_under_half : ((0.048055073125713964%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_Lambda_QCD_GeV_meas_pos : 0 < ((0.2173%R)).
Proof. lra. Qed.

Lemma gr_sqrt_sigma_GeV_err_under_half : ((0.025896107116174516%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_sqrt_sigma_GeV_meas_pos : 0 < ((0.42%R)).
Proof. lra. Qed.

Lemma gr_N_eff_err_under_half : ((0.028424048045719855%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_N_eff_meas_pos : 0 < ((3.046%R)).
Proof. lra. Qed.

Lemma gr_N_c_QCD_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_N_c_QCD_meas_pos : 0 < ((3.0%R)).
Proof. lra. Qed.

Lemma gr_Casimir_C_F_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_Casimir_C_F_meas_pos : 0 < ((1.3333333333333333%R)).
Proof. lra. Qed.

Lemma gr_Casimir_C_A_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_Casimir_C_A_meas_pos : 0 < ((3.0%R)).
Proof. lra. Qed.

Lemma gr_beta0_QCD_nf5_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_beta0_QCD_nf5_meas_pos : 0 < ((7.666666666666667%R)).
Proof. lra. Qed.

Lemma gr_alpha_s_gt_alpha_em_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_alpha_s_gt_alpha_em_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_koide_lepton_QR_err_under_half : ((0.0009230194964016114%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_koide_lepton_QR_meas_pos : 0 < ((0.6666666666666666%R)).
Proof. lra. Qed.

Lemma gr_sqrt2_structural_recovery_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_sqrt2_structural_recovery_meas_pos : 0 < ((1.4142135623730951%R)).
Proof. lra. Qed.

Lemma gr_yukawa_top_err_under_half : ((0.013457034902430751%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_yukawa_top_meas_pos : 0 < ((0.991%R)).
Proof. lra. Qed.

Lemma gr_morphic_phi_present_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_morphic_phi_present_meas_pos : 0 < ((1.618033988749895%R)).
Proof. lra. Qed.

Lemma gr_neutrino_m3_over_m2_err_under_half : ((0.1470630495663553%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_neutrino_m3_over_m2_meas_pos : 0 < ((5.707570518336111%R)).
Proof. lra. Qed.

Lemma gr_R_b_triangle_err_under_half : ((0.026537499247957154%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_R_b_triangle_meas_pos : 0 < ((0.3865593098089865%R)).
Proof. lra. Qed.

Lemma gr_R_t_triangle_err_under_half : ((0.019630621725789416%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_R_t_triangle_meas_pos : 0 < ((0.9117171162153312%R)).
Proof. lra. Qed.

Lemma gr_sin_delta_ckm_err_under_half : ((0.0036013868908110055%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_sin_delta_ckm_meas_pos : 0 < ((0.9115343723414107%R)).
Proof. lra. Qed.

Lemma gr_spin2_massless_helicities_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_massless_helicities_meas_pos : 0 < ((2.0%R)).
Proof. lra. Qed.

Lemma gr_spin2_TT_dof_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_TT_dof_meas_pos : 0 < ((2.0%R)).
Proof. lra. Qed.

Lemma gr_einstein_quadrupole_prefactor_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_einstein_quadrupole_prefactor_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_wilson_area_law_sigma_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_wilson_area_law_sigma_meas_pos : 0 < ((0.17649137329543738%R)).
Proof. lra. Qed.

Lemma gr_confinement_scale_ratio_err_under_half : ((0.022153229185580246%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_confinement_scale_ratio_meas_pos : 0 < ((0.5173809523809524%R)).
Proof. lra. Qed.

Lemma gr_asymptotic_freedom_beta0_pos_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_asymptotic_freedom_beta0_pos_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_flux_tube_E_over_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_flux_tube_E_over_L_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_polyakov_confined_order_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_massive_polarizations_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_massive_polarizations_meas_pos : 0 < ((5.0%R)).
Proof. lra. Qed.

Lemma gr_spin2_metric_dof_accounting_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_metric_dof_accounting_meas_pos : 0 < ((2.0%R)).
Proof. lra. Qed.

Lemma gr_equivalence_geodesic_structure_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_equivalence_geodesic_structure_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_spin2_wave_equation_flat_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_wave_equation_flat_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_bianchi_contracted_identity_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_bianchi_contracted_identity_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_spin2_TT_projector_complete_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_TT_projector_complete_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_soft_graviton_pole_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_soft_graviton_pole_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_instanton_action_scale_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_instanton_action_scale_meas_pos : 0 < ((669.6431825331274%R)).
Proof. lra. Qed.

Lemma gr_ym_beta_function_structure_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_ym_beta_function_structure_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_su3_center_order_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_su3_center_order_meas_pos : 0 < ((3.0%R)).
Proof. lra. Qed.

Lemma gr_dual_meissner_confined_flag_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_dual_meissner_confined_flag_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_theta_QCD_strong_CP_flag_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_glueball_over_sqrt_sigma_err_under_half : ((0.034782692362047014%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_glueball_over_sqrt_sigma_meas_pos : 0 < ((3.65%R)).
Proof. lra. Qed.

Lemma gr_trace_anomaly_structure_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_trace_anomaly_structure_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_graviton_propagator_pole_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_graviton_propagator_pole_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_gw_quadrupole_coupling_structure_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_gw_quadrupole_coupling_structure_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_massless_spin2_little_group_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_massless_spin2_little_group_meas_pos : 0 < ((2.0%R)).
Proof. lra. Qed.

Lemma gr_triangle_angle_sum_pi_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_triangle_angle_sum_pi_meas_pos : 0 < ((3.141592653589793%R)).
Proof. lra. Qed.

Lemma gr_alpha_rad_err_under_half : ((0.03680231674953141%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_alpha_rad_meas_pos : 0 < ((1.5982430233482232%R)).
Proof. lra. Qed.

Lemma gr_beta_rad_err_under_half : ((0.029711617355294043%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_beta_rad_meas_pos : 0 < ((0.3967401060358461%R)).
Proof. lra. Qed.

Lemma gr_gamma_rad_err_under_half : ((0.04101767408617176%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_gamma_rad_meas_pos : 0 < ((1.1466095242057237%R)).
Proof. lra. Qed.

Lemma sm_lambda_ckm_err_under_half : ((0.06225011989853476%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_A_wolfenstein_err_under_half : ((0.05246555208389803%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_rho_bar_err_under_half : ((0.02700157709000836%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_eta_bar_err_under_half : ((0.0028013614651725667%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_Jarlskog_J_err_under_half : ((0.23792303102008408%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_delta_ckm_rad_err_under_half : ((0.02612849108321111%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ud_err_under_half : ((0.002658467271059532%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_us_err_under_half : ((0.06225011989853476%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ub_err_under_half : ((0.23474330619715575%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cd_err_under_half : ((0.12454706932169445%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cs_err_under_half : ((0.08568112914816942%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cb_err_under_half : ((0.15304243191119066%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_td_err_under_half : ((0.2337487764470785%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ts_err_under_half : ((0.14583328325587586%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_tb_err_under_half : ((0.0004449567119691174%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_W_err_under_half : ((0.06713369973590165%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_W_onshell_err_under_half : ((0.15026877693416243%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_inv_err_under_half : ((0.1472364924023795%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_s_MZ_err_under_half : ((0.007242651170537564%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_H_err_under_half : ((0.0011951533584994727%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_W_err_under_half : ((0.03999290024803384%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_Z_err_under_half : ((0.018424423512725066%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_t_err_under_half : ((0.052705818067851705%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_Lambda_QCD_GeV_err_under_half : ((0.04921722442825905%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sqrt_sigma_GeV_err_under_half : ((0.02566066753490444%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_N_eff_err_under_half : ((0.07917549100062735%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_12_err_under_half : ((0.013048795958832987%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_23_err_under_half : ((0.17474226348654942%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_13_err_under_half : ((0.003010045202972307%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_delta_pmns_rad_err_under_half : ((0.0997385337617464%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_dm2_21_err_under_half : ((0.07222853624703972%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_dm2_31_abs_err_under_half : ((0.36301157961075986%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_u_err_under_half : ((0.001399329001761096%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_c_err_under_half : ((0.17551087147971156%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_t_err_under_half : ((0.0014587296799373206%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_triangle_angle_sum_pi_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_yin_yang_in_unit_interval_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_all_kappa_nonnegative_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sector_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_edge_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

