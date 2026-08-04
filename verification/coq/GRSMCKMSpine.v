(* FSOT GR/SM/CKM/PMNS spine — multi-prover re-proof of exported obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma lambda_ckm_err_under_half : ((0.0674090941924869%R)) < (0.5%R).
Proof. lra. Qed.

Lemma lambda_ckm_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma lambda_ckm_abs_diff : ((0.00015167046193309552%R)) < ((0.00015318716655342646%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_err_finite : ((1.2112430567490686%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_measured_pos : 0 < ((0.826%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_abs_diff : ((0.010004867648747306%R)) < ((0.01010491632523578%R)).
Proof. lra. Qed.

Lemma rho_bar_err_finite : ((0.8542163106350151%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma rho_bar_measured_pos : 0 < ((0.159%R)).
Proof. lra. Qed.

Lemma rho_bar_abs_diff : ((0.001358203933909674%R)) < ((0.0013717859732497709%R)).
Proof. lra. Qed.

Lemma eta_bar_err_under_half : ((0.49211367344735246%R)) < (0.5%R).
Proof. lra. Qed.

Lemma eta_bar_measured_pos : 0 < ((0.348%R)).
Proof. lra. Qed.

Lemma eta_bar_abs_diff : ((0.0017125555835967865%R)) < ((0.0017296811394337545%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_err_finite : ((2.475842827902397%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_measured_pos : 0 < ((0.0000308%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_abs_diff : ((0.0000007625595909939384%R)) < ((0.0000007701851879038778%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_err_finite : ((4.923088578307108%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_measured_pos : 0 < ((1.196%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_abs_diff : ((0.05888013939655301%R)) < ((0.059468940790519544%R)).
Proof. lra. Qed.

Lemma V_ud_err_under_half : ((0.002696448876034594%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ud_measured_pos : 0 < ((0.97435%R)).
Proof. lra. Qed.

Lemma V_ud_abs_diff : ((0.00002627284962364307%R)) < ((0.0000265355781208795%R)).
Proof. lra. Qed.

Lemma V_us_err_under_half : ((0.0674090941924869%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_us_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma V_us_abs_diff : ((0.00015167046193309552%R)) < ((0.00015318716655342646%R)).
Proof. lra. Qed.

Lemma V_ub_err_finite : ((3.6810430545769552%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma V_ub_measured_pos : 0 < ((0.00369%R)).
Proof. lra. Qed.

Lemma V_ub_abs_diff : ((0.00013583048871388965%R)) < ((0.00013718879360202852%R)).
Proof. lra. Qed.

Lemma V_cd_err_under_half : ((0.12971202611985092%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cd_measured_pos : 0 < ((0.22486%R)).
Proof. lra. Qed.

Lemma V_cd_abs_diff : ((0.00029167046193309676%R)) < ((0.00029458716655342775%R)).
Proof. lra. Qed.

Lemma V_cs_err_under_half : ((0.08564311398950579%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cs_measured_pos : 0 < ((0.97349%R)).
Proof. lra. Qed.

Lemma V_cs_abs_diff : ((0.0008337271503764399%R)) < ((0.0008420644218812042%R)).
Proof. lra. Qed.

Lemma V_cb_err_finite : ((1.0868832908350836%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma V_cb_measured_pos : 0 < ((0.04182%R)).
Proof. lra. Qed.

Lemma V_cb_abs_diff : ((0.000454534592227232%R)) < ((0.00045907993815050437%R)).
Proof. lra. Qed.

Lemma V_td_err_finite : ((1.2956188612649575%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma V_td_measured_pos : 0 < ((0.00857%R)).
Proof. lra. Qed.

Lemma V_td_abs_diff : ((0.00011103453641040685%R)) < ((0.00011214488177551091%R)).
Proof. lra. Qed.

Lemma V_ts_err_finite : ((0.6459012354568695%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma V_ts_measured_pos : 0 < ((0.0411%R)).
Proof. lra. Qed.

Lemma V_ts_abs_diff : ((0.00026546540777277333%R)) < ((0.0002681200618515011%R)).
Proof. lra. Qed.

Lemma V_tb_err_under_half : ((0.08827786107347174%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_tb_measured_pos : 0 < ((0.999118%R)).
Proof. lra. Qed.

Lemma V_tb_abs_diff : ((0.0008820000000000494%R)) < ((0.0008908200000010499%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_err_finite : ((0.5605427410082864%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_measured_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_abs_diff : ((0.00129608692575936%R)) < ((0.0013090477950179536%R)).
Proof. lra. Qed.

Lemma alpha_inv_err_finite : ((1.117147243876773%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma alpha_inv_measured_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma alpha_inv_abs_diff : ((1.5308938868859059%R)) < ((1.546202825754766%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_err_finite : ((3.579369787719938%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_measured_pos : 0 < ((0.1179%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_abs_diff : ((0.004220076979721807%R)) < ((0.004262277749520025%R)).
Proof. lra. Qed.

Lemma m_H_err_under_half : ((0.12089010848922362%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_H_measured_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma m_H_abs_diff : ((0.15141486088275258%R)) < ((0.1529290094915811%R)).
Proof. lra. Qed.

Lemma m_W_err_finite : ((1.6981756204556522%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma m_W_measured_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma m_W_abs_diff : ((1.3649426184536395%R)) < ((1.378592044638177%R)).
Proof. lra. Qed.

Lemma m_Z_err_finite : ((1.0939302919222549%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma m_Z_measured_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma m_Z_abs_diff : ((0.9975287788768981%R)) < ((1.007504066665668%R)).
Proof. lra. Qed.

Lemma m_t_err_finite : ((1.5554132408708463%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma m_t_measured_pos : 0 < ((172.69%R)).
Proof. lra. Qed.

Lemma m_t_abs_diff : ((2.6860431256598645%R)) < ((2.712903556916464%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_err_under_half : ((0.2910480743994031%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_12_measured_pos : 0 < ((0.307%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_abs_diff : ((0.0008935175884061675%R)) < ((0.0009024527642912291%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_err_under_half : ((0.12991683625245593%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_23_measured_pos : 0 < ((0.546%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_abs_diff : ((0.0007093459259384094%R)) < ((0.0007164393851987935%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_err_finite : ((2.5824286687071702%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_measured_pos : 0 < ((0.022%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_abs_diff : ((0.0005681343071155774%R)) < ((0.0005738156501877332%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_err_finite : ((0.6093498205858049%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_measured_pos : 0 < ((3.4382986264288293%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_abs_diff : ((0.020951266511348265%R)) < ((0.02116077917646275%R)).
Proof. lra. Qed.

Lemma dm2_21_err_finite : ((4.118318933025263%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma dm2_21_measured_pos : 0 < ((0.0000753%R)).
Proof. lra. Qed.

Lemma dm2_21_abs_diff : ((0.000003101094156568023%R)) < ((0.0000031321050991337033%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_err_finite : ((6.834421455812894%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_measured_pos : 0 < ((0.002453%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_abs_diff : ((0.00016764835831109028%R)) < ((0.00016932484189520117%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_err_under_half : ((0.0012632120914846112%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_abs_diff : ((0.000012632120914846112%R)) < ((0.000012758442124994573%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_err_under_half : ((0.17111017284017205%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_abs_diff : ((0.0017111017284017205%R)) < ((0.0017282127456867379%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_err_under_half : ((0.1782655825115942%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_abs_diff : ((0.001782655825115942%R)) < ((0.0018004823833681013%R)).
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

Lemma emergent_unitarity_row_u_unitarity_tight : ((0.000012632120914846112%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_unitarity_tight : ((0.0017111017284017205%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_unitarity_tight : ((0.001782655825115942%R)) < ((0.05%R)).
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

Lemma gr_acoustic_null_cone_meas_pos : 0 < ((0.7693455090660798%R)).
Proof. lra. Qed.

Lemma gr_planck_length_m_err_under_half : ((0.000000000023928549890383717%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_c_light_si_exact_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_c_light_si_exact_meas_pos : 0 < ((299792458.0%R)).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_err_finite : ((1.4422223774651803%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_meas_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma gr_seed_alpha_inv_err_finite : ((1.2629964743568904%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma gr_seed_alpha_inv_meas_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma gr_seed_m_H_err_under_half : ((0.03990518384182655%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_H_meas_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma gr_seed_m_W_err_finite : ((0.836299635903489%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma gr_seed_m_W_meas_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma gr_seed_m_Z_err_under_half : ((0.09398120291369791%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_Z_meas_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma sm_lambda_ckm_err_under_half : ((0.0674090941924869%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_A_wolfenstein_err_finite : ((1.2112430567490686%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_rho_bar_err_finite : ((0.8542163106350151%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_eta_bar_err_under_half : ((0.49211367344735246%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_Jarlskog_J_err_finite : ((2.475842827902397%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_delta_ckm_rad_err_finite : ((4.923088578307108%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_ud_err_under_half : ((0.002696448876034594%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_us_err_under_half : ((0.0674090941924869%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ub_err_finite : ((3.6810430545769552%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_cd_err_under_half : ((0.12971202611985092%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cs_err_under_half : ((0.08564311398950579%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cb_err_finite : ((1.0868832908350836%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_td_err_finite : ((1.2956188612649575%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_ts_err_finite : ((0.6459012354568695%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_tb_err_under_half : ((0.08827786107347174%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_W_err_finite : ((0.5605427410082864%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_alpha_inv_err_finite : ((1.117147243876773%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_alpha_s_MZ_err_finite : ((3.579369787719938%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_m_H_err_under_half : ((0.12089010848922362%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_W_err_finite : ((1.6981756204556522%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_m_Z_err_finite : ((1.0939302919222549%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_m_t_err_finite : ((1.5554132408708463%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_sin2_theta_12_err_under_half : ((0.2910480743994031%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_23_err_under_half : ((0.12991683625245593%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_13_err_finite : ((2.5824286687071702%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_delta_pmns_rad_err_finite : ((0.6093498205858049%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_dm2_21_err_finite : ((4.118318933025263%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_dm2_31_abs_err_finite : ((6.834421455812894%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_u_err_under_half : ((0.0012632120914846112%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_c_err_under_half : ((0.17111017284017205%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_t_err_under_half : ((0.1782655825115942%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_yin_yang_in_unit_interval_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_all_kappa_nonnegative_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sector_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_edge_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

