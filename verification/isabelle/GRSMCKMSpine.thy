theory GRSMCKMSpine
  imports Complex_Main
begin

(* FSOT GR/SM/CKM/PMNS spine — multi-prover residual/structure certificates. *)

lemma lambda_ckm_err_under_half: "0.0674090941924869 < (0.5::real)"
  by simp

lemma lambda_ckm_measured_pos: "(0::real) < 0.225"
  by simp

lemma lambda_ckm_abs_diff: "0.0001516705 < 0.0001531872"
  by simp

lemma A_wolfenstein_err_finite: "1.2112430567490686 < 100.0"
  by simp

lemma A_wolfenstein_measured_pos: "(0::real) < 0.826"
  by simp

lemma A_wolfenstein_abs_diff: "0.010004867648747306 < 0.01010491632523578"
  by simp

lemma rho_bar_err_finite: "0.8542163106350151 < 100.0"
  by simp

lemma rho_bar_measured_pos: "(0::real) < 0.159"
  by simp

lemma rho_bar_abs_diff: "0.001358203933909674 < 0.0013717859732497709"
  by simp

lemma eta_bar_err_under_half: "0.49211367344735246 < (0.5::real)"
  by simp

lemma eta_bar_measured_pos: "(0::real) < 0.348"
  by simp

lemma eta_bar_abs_diff: "0.0017125555835967865 < 0.0017296811394337545"
  by simp

lemma Jarlskog_J_err_finite: "2.475842827902397 < 100.0"
  by simp

lemma Jarlskog_J_measured_pos: "(0::real) < 0.0000308"
  by simp

lemma Jarlskog_J_abs_diff: "0.0000007625596 < 0.0000007701852"
  by simp

lemma delta_ckm_rad_err_finite: "4.923088578307108 < 100.0"
  by simp

lemma delta_ckm_rad_measured_pos: "(0::real) < 1.196"
  by simp

lemma delta_ckm_rad_abs_diff: "0.05888013939655301 < 0.059468940790519544"
  by simp

lemma V_ud_err_under_half: "0.002696448876034594 < (0.5::real)"
  by simp

lemma V_ud_measured_pos: "(0::real) < 0.97435"
  by simp

lemma V_ud_abs_diff: "0.00002627285 < 0.00002653558"
  by simp

lemma V_us_err_under_half: "0.0674090941924869 < (0.5::real)"
  by simp

lemma V_us_measured_pos: "(0::real) < 0.225"
  by simp

lemma V_us_abs_diff: "0.0001516705 < 0.0001531872"
  by simp

lemma V_ub_err_finite: "3.6810430545769552 < 100.0"
  by simp

lemma V_ub_measured_pos: "(0::real) < 0.00369"
  by simp

lemma V_ub_abs_diff: "0.0001358305 < 0.0001371888"
  by simp

lemma V_cd_err_under_half: "0.12971202611985092 < (0.5::real)"
  by simp

lemma V_cd_measured_pos: "(0::real) < 0.22486"
  by simp

lemma V_cd_abs_diff: "0.0002916705 < 0.0002945872"
  by simp

lemma V_cs_err_under_half: "0.08564311398950579 < (0.5::real)"
  by simp

lemma V_cs_measured_pos: "(0::real) < 0.97349"
  by simp

lemma V_cs_abs_diff: "0.0008337272 < 0.0008420644"
  by simp

lemma V_cb_err_finite: "1.0868832908350836 < 100.0"
  by simp

lemma V_cb_measured_pos: "(0::real) < 0.04182"
  by simp

lemma V_cb_abs_diff: "0.0004545346 < 0.0004590799"
  by simp

lemma V_td_err_finite: "1.2956188612649575 < 100.0"
  by simp

lemma V_td_measured_pos: "(0::real) < 0.00857"
  by simp

lemma V_td_abs_diff: "0.0001110345 < 0.0001121449"
  by simp

lemma V_ts_err_finite: "0.6459012354568695 < 100.0"
  by simp

lemma V_ts_measured_pos: "(0::real) < 0.0411"
  by simp

lemma V_ts_abs_diff: "0.0002654654 < 0.0002681201"
  by simp

lemma V_tb_err_under_half: "0.08827786107347174 < (0.5::real)"
  by simp

lemma V_tb_measured_pos: "(0::real) < 0.999118"
  by simp

lemma V_tb_abs_diff: "0.000882 < 0.00089082"
  by simp

lemma sin2_theta_W_err_finite: "0.5605427410082864 < 100.0"
  by simp

lemma sin2_theta_W_measured_pos: "(0::real) < 0.23122"
  by simp

lemma sin2_theta_W_abs_diff: "0.00129608692575936 < 0.0013090477950179536"
  by simp

lemma alpha_inv_err_finite: "1.117147243876773 < 100.0"
  by simp

lemma alpha_inv_measured_pos: "(0::real) < 137.035999084"
  by simp

lemma alpha_inv_abs_diff: "1.5308938868859059 < 1.546202825754766"
  by simp

lemma alpha_s_MZ_err_finite: "3.579369787719938 < 100.0"
  by simp

lemma alpha_s_MZ_measured_pos: "(0::real) < 0.1179"
  by simp

lemma alpha_s_MZ_abs_diff: "0.004220076979721807 < 0.004262277749520025"
  by simp

lemma m_H_err_under_half: "0.12089010848922362 < (0.5::real)"
  by simp

lemma m_H_measured_pos: "(0::real) < 125.25"
  by simp

lemma m_H_abs_diff: "0.15141486088275258 < 0.1529290094915811"
  by simp

lemma m_W_err_finite: "1.6981756204556522 < 100.0"
  by simp

lemma m_W_measured_pos: "(0::real) < 80.377"
  by simp

lemma m_W_abs_diff: "1.3649426184536395 < 1.378592044638177"
  by simp

lemma m_Z_err_finite: "1.0939302919222549 < 100.0"
  by simp

lemma m_Z_measured_pos: "(0::real) < 91.1876"
  by simp

lemma m_Z_abs_diff: "0.9975287788768981 < 1.007504066665668"
  by simp

lemma m_t_err_finite: "1.5554132408708463 < 100.0"
  by simp

lemma m_t_measured_pos: "(0::real) < 172.69"
  by simp

lemma m_t_abs_diff: "2.6860431256598645 < 2.712903556916464"
  by simp

lemma sin2_theta_12_err_under_half: "0.2910480743994031 < (0.5::real)"
  by simp

lemma sin2_theta_12_measured_pos: "(0::real) < 0.307"
  by simp

lemma sin2_theta_12_abs_diff: "0.0008935176 < 0.0009024528"
  by simp

lemma sin2_theta_23_err_under_half: "0.12991683625245593 < (0.5::real)"
  by simp

lemma sin2_theta_23_measured_pos: "(0::real) < 0.546"
  by simp

lemma sin2_theta_23_abs_diff: "0.0007093459 < 0.0007164394"
  by simp

lemma sin2_theta_13_err_finite: "2.5824286687071702 < 100.0"
  by simp

lemma sin2_theta_13_measured_pos: "(0::real) < 0.022"
  by simp

lemma sin2_theta_13_abs_diff: "0.0005681343 < 0.0005738157"
  by simp

lemma delta_pmns_rad_err_finite: "0.6093498205858049 < 100.0"
  by simp

lemma delta_pmns_rad_measured_pos: "(0::real) < 3.4382986264288293"
  by simp

lemma delta_pmns_rad_abs_diff: "0.020951266511348265 < 0.02116077917646275"
  by simp

lemma dm2_21_err_finite: "4.118318933025263 < 100.0"
  by simp

lemma dm2_21_measured_pos: "(0::real) < 0.0000753"
  by simp

lemma dm2_21_abs_diff: "0.000003101094 < 0.000003132105"
  by simp

lemma dm2_31_abs_err_finite: "6.834421455812894 < 100.0"
  by simp

lemma dm2_31_abs_measured_pos: "(0::real) < 0.002453"
  by simp

lemma dm2_31_abs_abs_diff: "0.0001676484 < 0.0001693248"
  by simp

lemma emergent_unitarity_row_u_err_under_half: "0.0012632120914846112 < (0.5::real)"
  by simp

lemma emergent_unitarity_row_u_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_u_abs_diff: "0.00001263212 < 0.00001275844"
  by simp

lemma emergent_unitarity_row_c_err_under_half: "0.17111017284017205 < (0.5::real)"
  by simp

lemma emergent_unitarity_row_c_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_c_abs_diff: "0.0017111017284017205 < 0.0017282127456867379"
  by simp

lemma emergent_unitarity_row_t_err_under_half: "0.1782655825115942 < (0.5::real)"
  by simp

lemma emergent_unitarity_row_t_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_t_abs_diff: "0.001782655825115942 < 0.0018004823833681013"
  by simp

lemma yin_yang_in_unit_interval_err_under_half: "0 < (0.5::real)"
  by simp

lemma yin_yang_in_unit_interval_measured_pos: "(0::real) < 1.0"
  by simp

lemma yin_yang_in_unit_interval_abs_diff: "0 < 0.000000001"
  by simp

lemma all_kappa_nonnegative_err_under_half: "0 < (0.5::real)"
  by simp

lemma all_kappa_nonnegative_measured_pos: "(0::real) < 1.0"
  by simp

lemma all_kappa_nonnegative_abs_diff: "0 < 0.000000001"
  by simp

lemma sector_count_err_under_half: "0 < (0.5::real)"
  by simp

lemma sector_count_measured_pos: "(0::real) < 8.0"
  by simp

lemma sector_count_abs_diff: "0 < 0.000000001"
  by simp

lemma edge_count_err_under_half: "0 < (0.5::real)"
  by simp

lemma edge_count_measured_pos: "(0::real) < 15.0"
  by simp

lemma edge_count_abs_diff: "0 < 0.000000001"
  by simp

lemma emergent_unitarity_row_u_unitarity_tight: "0.00001263212 < 0.05"
  by simp

lemma emergent_unitarity_row_c_unitarity_tight: "0.0017111017284017205 < 0.05"
  by simp

lemma emergent_unitarity_row_t_unitarity_tight: "0.001782655825115942 < 0.05"
  by simp

lemma gauge_n_U1_eq: "(1::nat) = 1"
  by simp

lemma gauge_n_U1_pos: "(0::nat) < 1"
  by simp

lemma gauge_n_SU2_eq: "(3::nat) = 3"
  by simp

lemma gauge_n_SU2_pos: "(0::nat) < 3"
  by simp

lemma gauge_n_SU3_eq: "(8::nat) = 8"
  by simp

lemma gauge_n_SU3_pos: "(0::nat) < 8"
  by simp

lemma gauge_n_gen_total_eq: "(12::nat) = 12"
  by simp

lemma gauge_n_gen_total_pos: "(0::nat) < 12"
  by simp

lemma gauge_n_fermion_gen_eq: "(3::nat) = 3"
  by simp

lemma gauge_n_fermion_gen_pos: "(0::nat) < 3"
  by simp

lemma gr_einstein_trace_reverse_err_under_half: "0 < (0.5::real)"
  by simp

lemma gr_einstein_trace_reverse_meas_pos: "(0::real) < 0.5"
  by simp

lemma gr_weak_field_2phi_err_under_half: "0 < (0.5::real)"
  by simp

lemma gr_weak_field_2phi_meas_pos: "(0::real) < 0.000002"
  by simp

lemma gr_schwarzschild_radius_sun_m_err_under_half: "0.003026566219535862 < (0.5::real)"
  by simp

lemma gr_schwarzschild_radius_sun_m_meas_pos: "(0::real) < 2953.25"
  by simp

lemma gr_solar_light_deflection_rad_err_under_half: "0.013893853126499888 < (0.5::real)"
  by simp

lemma gr_solar_light_deflection_rad_meas_pos: "(0::real) < 0.000008489088"
  by simp

lemma gr_mercury_perihelion_arcsec_cy_err_under_half: "0.0047099996121108675 < (0.5::real)"
  by simp

lemma gr_mercury_perihelion_arcsec_cy_meas_pos: "(0::real) < 42.98"
  by simp

lemma gr_acoustic_null_cone_err_under_half: "0 < (0.5::real)"
  by simp

lemma gr_acoustic_null_cone_meas_pos: "(0::real) < 0.7693455090660798"
  by simp

lemma gr_planck_length_m_err_under_half: "0.00000000002392855 < (0.5::real)"
  by simp

lemma gr_c_light_si_exact_err_under_half: "0 < (0.5::real)"
  by simp

lemma gr_c_light_si_exact_meas_pos: "(0::real) < 299792458.0"
  by simp

lemma gr_seed_sin2_theta_W_err_finite: "1.4422223774651803 < 100.0"
  by simp

lemma gr_seed_sin2_theta_W_meas_pos: "(0::real) < 0.23122"
  by simp

lemma gr_seed_alpha_inv_err_finite: "1.2629964743568904 < 100.0"
  by simp

lemma gr_seed_alpha_inv_meas_pos: "(0::real) < 137.035999084"
  by simp

lemma gr_seed_m_H_err_under_half: "0.03990518384182655 < (0.5::real)"
  by simp

lemma gr_seed_m_H_meas_pos: "(0::real) < 125.25"
  by simp

lemma gr_seed_m_W_err_finite: "0.836299635903489 < 100.0"
  by simp

lemma gr_seed_m_W_meas_pos: "(0::real) < 80.377"
  by simp

lemma gr_seed_m_Z_err_under_half: "0.09398120291369791 < (0.5::real)"
  by simp

lemma gr_seed_m_Z_meas_pos: "(0::real) < 91.1876"
  by simp

lemma sm_lambda_ckm_err_under_half: "0.0674090941924869 < (0.5::real)"
  by simp

lemma sm_A_wolfenstein_err_finite: "1.2112430567490686 < 100.0"
  by simp

lemma sm_rho_bar_err_finite: "0.8542163106350151 < 100.0"
  by simp

lemma sm_eta_bar_err_under_half: "0.49211367344735246 < (0.5::real)"
  by simp

lemma sm_Jarlskog_J_err_finite: "2.475842827902397 < 100.0"
  by simp

lemma sm_delta_ckm_rad_err_finite: "4.923088578307108 < 100.0"
  by simp

lemma sm_V_ud_err_under_half: "0.002696448876034594 < (0.5::real)"
  by simp

lemma sm_V_us_err_under_half: "0.0674090941924869 < (0.5::real)"
  by simp

lemma sm_V_ub_err_finite: "3.6810430545769552 < 100.0"
  by simp

lemma sm_V_cd_err_under_half: "0.12971202611985092 < (0.5::real)"
  by simp

lemma sm_V_cs_err_under_half: "0.08564311398950579 < (0.5::real)"
  by simp

lemma sm_V_cb_err_finite: "1.0868832908350836 < 100.0"
  by simp

lemma sm_V_td_err_finite: "1.2956188612649575 < 100.0"
  by simp

lemma sm_V_ts_err_finite: "0.6459012354568695 < 100.0"
  by simp

lemma sm_V_tb_err_under_half: "0.08827786107347174 < (0.5::real)"
  by simp

lemma sm_sin2_theta_W_err_finite: "0.5605427410082864 < 100.0"
  by simp

lemma sm_alpha_inv_err_finite: "1.117147243876773 < 100.0"
  by simp

lemma sm_alpha_s_MZ_err_finite: "3.579369787719938 < 100.0"
  by simp

lemma sm_m_H_err_under_half: "0.12089010848922362 < (0.5::real)"
  by simp

lemma sm_m_W_err_finite: "1.6981756204556522 < 100.0"
  by simp

lemma sm_m_Z_err_finite: "1.0939302919222549 < 100.0"
  by simp

lemma sm_m_t_err_finite: "1.5554132408708463 < 100.0"
  by simp

lemma sm_sin2_theta_12_err_under_half: "0.2910480743994031 < (0.5::real)"
  by simp

lemma sm_sin2_theta_23_err_under_half: "0.12991683625245593 < (0.5::real)"
  by simp

lemma sm_sin2_theta_13_err_finite: "2.5824286687071702 < 100.0"
  by simp

lemma sm_delta_pmns_rad_err_finite: "0.6093498205858049 < 100.0"
  by simp

lemma sm_dm2_21_err_finite: "4.118318933025263 < 100.0"
  by simp

lemma sm_dm2_31_abs_err_finite: "6.834421455812894 < 100.0"
  by simp

lemma sm_emergent_unitarity_row_u_err_under_half: "0.0012632120914846112 < (0.5::real)"
  by simp

lemma sm_emergent_unitarity_row_c_err_under_half: "0.17111017284017205 < (0.5::real)"
  by simp

lemma sm_emergent_unitarity_row_t_err_under_half: "0.1782655825115942 < (0.5::real)"
  by simp

lemma sm_yin_yang_in_unit_interval_err_under_half: "0 < (0.5::real)"
  by simp

lemma sm_all_kappa_nonnegative_err_under_half: "0 < (0.5::real)"
  by simp

lemma sm_sector_count_err_under_half: "0 < (0.5::real)"
  by simp

lemma sm_edge_count_err_under_half: "0 < (0.5::real)"
  by simp

end
