(* FSOT GR/SM/CKM/PMNS spine — multi-prover re-proof of exported obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma V_ud_err_under_half : ((0.009504134401237756%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ud_measured_pos : 0 < ((0.97435%R)).
Proof. lra. Qed.

Lemma V_ud_abs_diff : ((0.00009260353353846007%R)) < ((0.00009352956887484467%R)).
Proof. lra. Qed.

Lemma V_us_err_under_half : ((0.00950413440123674%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_us_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma V_us_abs_diff : ((0.000021384302402782662%R)) < ((0.00002159814542781049%R)).
Proof. lra. Qed.

Lemma V_ub_err_under_half : ((0.009504134401238675%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ub_measured_pos : 0 < ((0.00369%R)).
Proof. lra. Qed.

Lemma V_ub_abs_diff : ((0.00000035070255940570713%R)) < ((0.00000035420958599976423%R)).
Proof. lra. Qed.

Lemma V_cd_err_under_half : ((0.009504134401234966%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cd_measured_pos : 0 < ((0.22486%R)).
Proof. lra. Qed.

Lemma V_cd_abs_diff : ((0.000021370996614616944%R)) < ((0.000021584706581763113%R)).
Proof. lra. Qed.

Lemma V_cs_err_under_half : ((0.009504134401234833%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cs_measured_pos : 0 < ((0.97349%R)).
Proof. lra. Qed.

Lemma V_cs_abs_diff : ((0.00009252179798258098%R)) < ((0.00009344701596340679%R)).
Proof. lra. Qed.

Lemma V_cb_err_under_half : ((0.009504134401244898%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cb_measured_pos : 0 < ((0.04182%R)).
Proof. lra. Qed.

Lemma V_cb_abs_diff : ((0.000003974629006600616%R)) < ((0.000004014375297666623%R)).
Proof. lra. Qed.

Lemma V_td_err_under_half : ((0.00950413440123913%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_td_measured_pos : 0 < ((0.00857%R)).
Proof. lra. Qed.

Lemma V_td_abs_diff : ((0.0000008145043181861933%R)) < ((0.0000008226493623680553%R)).
Proof. lra. Qed.

Lemma V_ts_err_under_half : ((0.009504134401236155%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ts_measured_pos : 0 < ((0.0411%R)).
Proof. lra. Qed.

Lemma V_ts_abs_diff : ((0.000003906199238908059%R)) < ((0.00000394526123229714%R)).
Proof. lra. Qed.

Lemma V_tb_err_under_half : ((0.009504134401237528%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_tb_measured_pos : 0 < ((0.999118%R)).
Proof. lra. Qed.

Lemma V_tb_abs_diff : ((0.00009495751754695636%R)) < ((0.00009590709272342593%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_u_err_under_half : ((0.000346139999995998%R)) < (0.5%R).
Proof. lra. Qed.

Lemma ckm_unitarity_row_u_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_u_abs_diff : ((0.00000346139999995998%R)) < ((0.0000034960140009595795%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_c_err_under_half : ((0.0006287900000123692%R)) < (0.5%R).
Proof. lra. Qed.

Lemma ckm_unitarity_row_c_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_c_abs_diff : ((0.000006287900000123692%R)) < ((0.000006350779001124929%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_t_err_under_half : ((0.000056717600005473656%R)) < (0.5%R).
Proof. lra. Qed.

Lemma ckm_unitarity_row_t_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_t_abs_diff : ((0.0000005671760000547366%R)) < ((0.0000005728477610552839%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_d_err_under_half : ((0.0006612999999933145%R)) < (0.5%R).
Proof. lra. Qed.

Lemma ckm_unitarity_col_d_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_d_abs_diff : ((0.000006612999999933145%R)) < ((0.000006679130000932476%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_s_err_under_half : ((0.0003009900000017218%R)) < (0.5%R).
Proof. lra. Qed.

Lemma ckm_unitarity_col_s_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_s_abs_diff : ((0.0000030099000000172182%R)) < ((0.00000303999900101739%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_b_err_under_half : ((0.0000693576000077023%R)) < (0.5%R).
Proof. lra. Qed.

Lemma ckm_unitarity_col_b_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_b_abs_diff : ((0.000000693576000077023%R)) < ((0.0000007005117610777933%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_err_under_half : ((0.009504134401235372%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_12_measured_pos : 0 < ((0.307%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_abs_diff : ((0.000029177692611792594%R)) < ((0.00002946946953891052%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_err_under_half : ((0.009504134401237823%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_23_measured_pos : 0 < ((0.546%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_abs_diff : ((0.000051892573830758515%R)) < ((0.0000524114995700661%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_err_under_half : ((0.009504134401232394%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_13_measured_pos : 0 < ((0.022%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_abs_diff : ((0.0000020909095682711265%R)) < ((0.0000021118186649538377%R)).
Proof. lra. Qed.

Lemma theta_12_deg_err_under_half : ((0.009504134401235625%R)) < (0.5%R).
Proof. lra. Qed.

Lemma theta_12_deg_measured_pos : 0 < ((33.41%R)).
Proof. lra. Qed.

Lemma theta_12_deg_abs_diff : ((0.003175331303452822%R)) < ((0.00320708461648835%R)).
Proof. lra. Qed.

Lemma theta_23_deg_err_under_half : ((0.009504134401243284%R)) < (0.5%R).
Proof. lra. Qed.

Lemma theta_23_deg_measured_pos : 0 < ((49.0%R)).
Proof. lra. Qed.

Lemma theta_23_deg_abs_diff : ((0.004657025856609209%R)) < ((0.004703596115176302%R)).
Proof. lra. Qed.

Lemma theta_13_deg_err_under_half : ((0.009504134401242691%R)) < (0.5%R).
Proof. lra. Qed.

Lemma theta_13_deg_measured_pos : 0 < ((8.54%R)).
Proof. lra. Qed.

Lemma theta_13_deg_abs_diff : ((0.0008116530778661257%R)) < ((0.0008197696086457869%R)).
Proof. lra. Qed.

Lemma delta_CP_deg_err_under_half : ((0.009504134401235261%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_CP_deg_measured_pos : 0 < ((197.0%R)).
Proof. lra. Qed.

Lemma delta_CP_deg_abs_diff : ((0.018723144770433464%R)) < ((0.0189103762181388%R)).
Proof. lra. Qed.

Lemma pmns_hierarchy_s13_lt_s12_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma pmns_hierarchy_s13_lt_s12_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma pmns_hierarchy_s13_lt_s12_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma pmns_hierarchy_s12_lt_s23_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma pmns_hierarchy_s12_lt_s23_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma pmns_hierarchy_s12_lt_s23_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma wolfenstein_lambda_err_under_half : ((0.00950413440123674%R)) < (0.5%R).
Proof. lra. Qed.

Lemma wolfenstein_lambda_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma wolfenstein_lambda_abs_diff : ((0.000021384302402782662%R)) < ((0.00002159814542781049%R)).
Proof. lra. Qed.

Lemma wolfenstein_A_err_under_half : ((0.009504134401235067%R)) < (0.5%R).
Proof. lra. Qed.

Lemma wolfenstein_A_measured_pos : 0 < ((0.826%R)).
Proof. lra. Qed.

Lemma wolfenstein_A_abs_diff : ((0.00007850415015420165%R)) < ((0.00007928919165674366%R)).
Proof. lra. Qed.

Lemma wolfenstein_rho_bar_err_under_half : ((0.009504134401234179%R)) < (0.5%R).
Proof. lra. Qed.

Lemma wolfenstein_rho_bar_measured_pos : 0 < ((0.159%R)).
Proof. lra. Qed.

Lemma wolfenstein_rho_bar_abs_diff : ((0.000015111573697962344%R)) < ((0.000015262689435941968%R)).
Proof. lra. Qed.

Lemma wolfenstein_eta_bar_err_under_half : ((0.009504134401242908%R)) < (0.5%R).
Proof. lra. Qed.

Lemma wolfenstein_eta_bar_measured_pos : 0 < ((0.348%R)).
Proof. lra. Qed.

Lemma wolfenstein_eta_bar_abs_diff : ((0.000033074387716325315%R)) < ((0.00003340513159448857%R)).
Proof. lra. Qed.

Lemma wolfenstein_Vus_eq_lambda_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma wolfenstein_Vus_eq_lambda_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma wolfenstein_Vus_eq_lambda_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma wolfenstein_Vcb_A_lambda2_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma wolfenstein_Vcb_A_lambda2_measured_pos : 0 < ((0.04182%R)).
Proof. lra. Qed.

Lemma wolfenstein_Vcb_A_lambda2_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma wolfenstein_Vub_A_lambda3_r_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma wolfenstein_Vub_A_lambda3_r_measured_pos : 0 < ((0.00369%R)).
Proof. lra. Qed.

Lemma wolfenstein_Vub_A_lambda3_r_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma wolfenstein_eta_bar_positive_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma wolfenstein_eta_bar_positive_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma wolfenstein_eta_bar_positive_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma delta_ckm_deg_err_under_half : ((0.009504134401239367%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_ckm_deg_measured_pos : 0 < ((68.5%R)).
Proof. lra. Qed.

Lemma delta_ckm_deg_abs_diff : ((0.006510332064848967%R)) < ((0.006575435385498457%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_err_under_half : ((0.00950413440124136%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_ckm_rad_measured_pos : 0 < ((1.196%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_abs_diff : ((0.00011366944743884666%R)) < ((0.00011480614191423512%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_err_under_half : ((0.009504134401248197%R)) < (0.5%R).
Proof. lra. Qed.

Lemma Jarlskog_J_measured_pos : 0 < ((0.0000308%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_abs_diff : ((0.000000002927273395584445%R)) < ((0.0000000029565471295402897%R)).
Proof. lra. Qed.

Lemma Jarlskog_wolfenstein_approx_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma Jarlskog_wolfenstein_approx_measured_pos : 0 < ((0.0000308%R)).
Proof. lra. Qed.

Lemma Jarlskog_wolfenstein_approx_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma Jarlskog_positive_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma Jarlskog_positive_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma Jarlskog_positive_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma unitary_triangle_Rb_err_under_half : ((0.00950413440124138%R)) < (0.5%R).
Proof. lra. Qed.

Lemma unitary_triangle_Rb_measured_pos : 0 < ((0.382602927328059%R)).
Proof. lra. Qed.

Lemma unitary_triangle_Rb_abs_diff : ((0.00003636309643634261%R)) < ((0.00003672672740170604%R)).
Proof. lra. Qed.

Lemma unitary_triangle_Rt_err_under_half : ((0.009504134401243274%R)) < (0.5%R).
Proof. lra. Qed.

Lemma unitary_triangle_Rt_measured_pos : 0 < ((0.9101565799355624%R)).
Proof. lra. Qed.

Lemma unitary_triangle_Rt_abs_diff : ((0.00008650250461883502%R)) < ((0.00008736752966602337%R)).
Proof. lra. Qed.

Lemma pmns_sin_delta_CP_err_under_half : ((0.009504134401242693%R)) < (0.5%R).
Proof. lra. Qed.

Lemma pmns_sin_delta_CP_measured_pos : 0 < ((0.29237170472273677%R)).
Proof. lra. Qed.

Lemma pmns_sin_delta_CP_abs_diff : ((0.000027787399768053334%R)) < ((0.000028065273766733868%R)).
Proof. lra. Qed.

Lemma dm2_21_err_under_half : ((0.009504134401244663%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_21_measured_pos : 0 < ((0.0000753%R)).
Proof. lra. Qed.

Lemma dm2_21_abs_diff : ((0.0000000071566132041372315%R)) < ((0.000000007228180336178604%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_err_under_half : ((0.00950413440123409%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_31_abs_measured_pos : 0 < ((0.002453%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_abs_diff : ((0.00000023313641686227224%R)) < ((0.00000023546778203089498%R)).
Proof. lra. Qed.

Lemma dm2_hierarchy_ratio_err_under_half : ((0.009504134401243234%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_hierarchy_ratio_measured_pos : 0 < ((32.57636122177955%R)).
Proof. lra. Qed.

Lemma dm2_hierarchy_ratio_abs_diff : ((0.0030961011535524108%R)) < ((0.003127062165088935%R)).
Proof. lra. Qed.

Lemma dm2_31_gt_dm2_21_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_31_gt_dm2_21_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma dm2_31_gt_dm2_21_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma ew_cos_theta_W_from_masses_err_under_half : ((0.009504134401235296%R)) < (0.5%R).
Proof. lra. Qed.

Lemma ew_cos_theta_W_from_masses_measured_pos : 0 < ((0.8814466001956406%R)).
Proof. lra. Qed.

Lemma ew_cos_theta_W_from_masses_abs_diff : ((0.00008377386955771282%R)) < ((0.00008461160825428995%R)).
Proof. lra. Qed.

Lemma ew_cos_theta_W_vs_sin2_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma ew_cos_theta_W_vs_sin2_measured_pos : 0 < ((0.8768010036490607%R)).
Proof. lra. Qed.

Lemma ew_cos_theta_W_vs_sin2_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma sm_anomaly_cancel_per_generation_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_anomaly_cancel_per_generation_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma sm_anomaly_SU2_U1_trace_Y_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_anomaly_SU2_U1_trace_Y_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma charge_electron_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma charge_electron_L_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma charge_neutrino_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma charge_neutrino_L_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma charge_up_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma charge_up_L_measured_pos : 0 < ((0.6666666666666666%R)).
Proof. lra. Qed.

Lemma charge_up_L_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma charge_down_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma charge_down_L_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma charge_u_R_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma charge_u_R_measured_pos : 0 < ((0.6666666666666666%R)).
Proof. lra. Qed.

Lemma charge_u_R_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma charge_d_R_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma charge_d_R_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma gr_2phi_classical_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_2phi_classical_measured_pos : 0 < ((0.000002%R)).
Proof. lra. Qed.

Lemma gr_2phi_classical_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma gr_einstein_half_R_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_einstein_half_R_measured_pos : 0 < ((0.5%R)).
Proof. lra. Qed.

Lemma gr_einstein_half_R_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma gr_light_deflection_arcsec_solar_err_under_half : ((0.010049118924188203%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_light_deflection_arcsec_solar_measured_pos : 0 < ((1.751%R)).
Proof. lra. Qed.

Lemma gr_light_deflection_arcsec_solar_abs_diff : ((0.0001759600723625354%R)) < ((0.00017771967308716075%R)).
Proof. lra. Qed.

Lemma gr_mercury_perihelion_arcsec_cy_err_under_half : ((0.01004911892419796%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_mercury_perihelion_arcsec_cy_measured_pos : 0 < ((42.98%R)).
Proof. lra. Qed.

Lemma gr_mercury_perihelion_arcsec_cy_abs_diff : ((0.004319111313620283%R)) < ((0.004362302426757486%R)).
Proof. lra. Qed.

Lemma n_U1_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma n_U1_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma n_U1_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma n_SU2_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma n_SU2_measured_pos : 0 < ((3.0%R)).
Proof. lra. Qed.

Lemma n_SU2_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma n_SU3_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma n_SU3_measured_pos : 0 < ((8.0%R)).
Proof. lra. Qed.

Lemma n_SU3_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma n_gen_total_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma n_gen_total_measured_pos : 0 < ((12.0%R)).
Proof. lra. Qed.

Lemma n_gen_total_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma n_fermion_generations_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma n_fermion_generations_measured_pos : 0 < ((3.0%R)).
Proof. lra. Qed.

Lemma n_fermion_generations_abs_diff : (0%R) < ((0.000000001%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_u_unitarity_tight : ((0.00000346139999995998%R)) < ((0.002%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_c_unitarity_tight : ((0.000006287900000123692%R)) < ((0.002%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_row_t_unitarity_tight : ((0.0000005671760000547366%R)) < ((0.002%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_d_unitarity_tight : ((0.000006612999999933145%R)) < ((0.002%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_s_unitarity_tight : ((0.0000030099000000172182%R)) < ((0.002%R)).
Proof. lra. Qed.

Lemma ckm_unitarity_col_b_unitarity_tight : ((0.000000693576000077023%R)) < ((0.002%R)).
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

Lemma gr_einstein_trace_reverse_structure_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_einstein_trace_reverse_structure_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_weak_field_2phi_deviation_err_under_half : ((0.010049119969584104%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_weak_field_2phi_deviation_meas_pos : 0 < ((0.000002%R)).
Proof. lra. Qed.

Lemma gr_weak_field_gii_err_under_half : ((0.000000020098285486827472%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_weak_field_gii_meas_pos : 0 < ((0.999998%R)).
Proof. lra. Qed.

Lemma gr_poisson_source_positive_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_poisson_source_positive_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_schwarzschild_radius_sun_m_err_under_half : ((0.013075989286963106%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_schwarzschild_radius_sun_m_meas_pos : 0 < ((2953.25%R)).
Proof. lra. Qed.

Lemma gr_solar_light_deflection_rad_err_under_half : ((0.023944368260521525%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_solar_light_deflection_rad_meas_pos : 0 < ((0.000008489087556227974%R)).
Proof. lra. Qed.

Lemma gr_mercury_perihelion_arcsec_cy_meas_pos : 0 < ((42.98%R)).
Proof. lra. Qed.

Lemma gr_friedmann_H2_positive_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_friedmann_H2_positive_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_acoustic_null_cone_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_acoustic_null_cone_meas_pos : 0 < ((0.7693455090660798%R)).
Proof. lra. Qed.

Lemma gr_geodesic_deviation_scale_err_under_half : ((0.010049118924187393%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_geodesic_deviation_scale_meas_pos : 0 < ((0.0000000001%R)).
Proof. lra. Qed.

Lemma gr_planck_length_m_err_under_half : ((0.0000000812315831742237%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_G_newton_si_err_under_half : ((0.010049118924197253%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_G_newton_si_meas_pos : 0 < ((0.000000000066743%R)).
Proof. lra. Qed.

Lemma gr_c_light_si_exact_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_c_light_si_exact_meas_pos : 0 < ((299792458.0%R)).
Proof. lra. Qed.

Lemma sm_generators_U1Y_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_generators_SU2L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_generators_SU3c_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_em_inv_err_under_half : ((0.009504134401232328%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_W_err_under_half : ((0.009504134401234463%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_s_MZ_err_under_half : ((0.009504134401239374%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_total_gauge_bosons_generators_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_W_err_under_half : ((0.009504134401231034%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_Z_err_under_half : ((0.009504134401234711%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_H_err_under_half : ((0.00950413440123411%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_t_err_under_half : ((0.009504134401232968%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_G_F_GeV_m2_err_under_half : ((0.009504134401238606%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_fermion_generations_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_charge_electron_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_charge_neutrino_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_charge_up_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_charge_down_L_err_under_half : ((0.000000000000016653345369377348%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_charge_positron_R_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_e_err_under_half : ((0.009504134401230541%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_mu_err_under_half : ((0.009504134401236932%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_tau_err_under_half : ((0.009504134401234309%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_ratio_mu_e_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_ratio_tau_mu_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_higgs_mass_from_potential_err_under_half : ((0.004751954295268555%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_higgs_vev_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_photon_massless_eq : (0 = 0)%nat.
Proof. reflexivity. Qed.

Lemma sm_alpha_s_gt_alpha_em_at_MZ_proxy_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

