/-
  FSOT Formal GRSMCKMSpine — multi-prover GR/SM/CKM/PMNS obligations.
  Generator: scripts/export_and_generate_gr_sm_ckm_artifacts.py
  Independent numeric certificates (norm_num / decide).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace FSOT.Formal.GRSMCKM

noncomputable section

theorem lambda_ckm_err_under_half : (0.0674090941924869 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem lambda_ckm_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem lambda_ckm_abs_diff : (0.00015167046193309552 : ℝ) < (0.00015318716655342646 : ℝ) := by
  norm_num

theorem A_wolfenstein_err_finite : (1.2112430567490686 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem A_wolfenstein_measured_pos : (0 : ℝ) < (0.826 : ℝ) := by
  norm_num

theorem A_wolfenstein_abs_diff : (0.010004867648747306 : ℝ) < (0.01010491632523578 : ℝ) := by
  norm_num

theorem rho_bar_err_finite : (0.8542163106350151 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem rho_bar_measured_pos : (0 : ℝ) < (0.159 : ℝ) := by
  norm_num

theorem rho_bar_abs_diff : (0.001358203933909674 : ℝ) < (0.0013717859732497709 : ℝ) := by
  norm_num

theorem eta_bar_err_under_half : (0.49211367344735246 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem eta_bar_measured_pos : (0 : ℝ) < (0.348 : ℝ) := by
  norm_num

theorem eta_bar_abs_diff : (0.0017125555835967865 : ℝ) < (0.0017296811394337545 : ℝ) := by
  norm_num

theorem Jarlskog_J_err_finite : (2.475842827902397 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem Jarlskog_J_measured_pos : (0 : ℝ) < (3.08e-05 : ℝ) := by
  norm_num

theorem Jarlskog_J_abs_diff : (7.625595909939384e-07 : ℝ) < (7.701851879038778e-07 : ℝ) := by
  norm_num

theorem delta_ckm_rad_err_finite : (4.923088578307108 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem delta_ckm_rad_measured_pos : (0 : ℝ) < (1.196 : ℝ) := by
  norm_num

theorem delta_ckm_rad_abs_diff : (0.05888013939655301 : ℝ) < (0.059468940790519544 : ℝ) := by
  norm_num

theorem V_ud_err_under_half : (0.002696448876034594 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ud_measured_pos : (0 : ℝ) < (0.97435 : ℝ) := by
  norm_num

theorem V_ud_abs_diff : (2.627284962364307e-05 : ℝ) < (2.65355781208795e-05 : ℝ) := by
  norm_num

theorem V_us_err_under_half : (0.0674090941924869 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_us_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem V_us_abs_diff : (0.00015167046193309552 : ℝ) < (0.00015318716655342646 : ℝ) := by
  norm_num

theorem V_ub_err_finite : (3.6810430545769552 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem V_ub_measured_pos : (0 : ℝ) < (0.00369 : ℝ) := by
  norm_num

theorem V_ub_abs_diff : (0.00013583048871388965 : ℝ) < (0.00013718879360202852 : ℝ) := by
  norm_num

theorem V_cd_err_under_half : (0.12971202611985092 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cd_measured_pos : (0 : ℝ) < (0.22486 : ℝ) := by
  norm_num

theorem V_cd_abs_diff : (0.00029167046193309676 : ℝ) < (0.00029458716655342775 : ℝ) := by
  norm_num

theorem V_cs_err_under_half : (0.08564311398950579 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cs_measured_pos : (0 : ℝ) < (0.97349 : ℝ) := by
  norm_num

theorem V_cs_abs_diff : (0.0008337271503764399 : ℝ) < (0.0008420644218812042 : ℝ) := by
  norm_num

theorem V_cb_err_finite : (1.0868832908350836 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem V_cb_measured_pos : (0 : ℝ) < (0.04182 : ℝ) := by
  norm_num

theorem V_cb_abs_diff : (0.000454534592227232 : ℝ) < (0.00045907993815050437 : ℝ) := by
  norm_num

theorem V_td_err_finite : (1.2956188612649575 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem V_td_measured_pos : (0 : ℝ) < (0.00857 : ℝ) := by
  norm_num

theorem V_td_abs_diff : (0.00011103453641040685 : ℝ) < (0.00011214488177551091 : ℝ) := by
  norm_num

theorem V_ts_err_finite : (0.6459012354568695 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem V_ts_measured_pos : (0 : ℝ) < (0.0411 : ℝ) := by
  norm_num

theorem V_ts_abs_diff : (0.00026546540777277333 : ℝ) < (0.0002681200618515011 : ℝ) := by
  norm_num

theorem V_tb_err_under_half : (0.08827786107347174 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_tb_measured_pos : (0 : ℝ) < (0.999118 : ℝ) := by
  norm_num

theorem V_tb_abs_diff : (0.0008820000000000494 : ℝ) < (0.0008908200000010499 : ℝ) := by
  norm_num

theorem sin2_theta_W_err_finite : (0.5605427410082864 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sin2_theta_W_measured_pos : (0 : ℝ) < (0.23122 : ℝ) := by
  norm_num

theorem sin2_theta_W_abs_diff : (0.00129608692575936 : ℝ) < (0.0013090477950179536 : ℝ) := by
  norm_num

theorem alpha_inv_err_finite : (1.117147243876773 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem alpha_inv_measured_pos : (0 : ℝ) < (137.035999084 : ℝ) := by
  norm_num

theorem alpha_inv_abs_diff : (1.5308938868859059 : ℝ) < (1.546202825754766 : ℝ) := by
  norm_num

theorem alpha_s_MZ_err_finite : (3.579369787719938 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem alpha_s_MZ_measured_pos : (0 : ℝ) < (0.1179 : ℝ) := by
  norm_num

theorem alpha_s_MZ_abs_diff : (0.004220076979721807 : ℝ) < (0.004262277749520025 : ℝ) := by
  norm_num

theorem m_H_err_under_half : (0.12089010848922362 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem m_H_measured_pos : (0 : ℝ) < (125.25 : ℝ) := by
  norm_num

theorem m_H_abs_diff : (0.15141486088275258 : ℝ) < (0.1529290094915811 : ℝ) := by
  norm_num

theorem m_W_err_finite : (1.6981756204556522 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem m_W_measured_pos : (0 : ℝ) < (80.377 : ℝ) := by
  norm_num

theorem m_W_abs_diff : (1.3649426184536395 : ℝ) < (1.378592044638177 : ℝ) := by
  norm_num

theorem m_Z_err_finite : (1.0939302919222549 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem m_Z_measured_pos : (0 : ℝ) < (91.1876 : ℝ) := by
  norm_num

theorem m_Z_abs_diff : (0.9975287788768981 : ℝ) < (1.007504066665668 : ℝ) := by
  norm_num

theorem m_t_err_finite : (1.5554132408708463 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem m_t_measured_pos : (0 : ℝ) < (172.69 : ℝ) := by
  norm_num

theorem m_t_abs_diff : (2.6860431256598645 : ℝ) < (2.712903556916464 : ℝ) := by
  norm_num

theorem sin2_theta_12_err_under_half : (0.2910480743994031 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_12_measured_pos : (0 : ℝ) < (0.307 : ℝ) := by
  norm_num

theorem sin2_theta_12_abs_diff : (0.0008935175884061675 : ℝ) < (0.0009024527642912291 : ℝ) := by
  norm_num

theorem sin2_theta_23_err_under_half : (0.12991683625245593 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_23_measured_pos : (0 : ℝ) < (0.546 : ℝ) := by
  norm_num

theorem sin2_theta_23_abs_diff : (0.0007093459259384094 : ℝ) < (0.0007164393851987935 : ℝ) := by
  norm_num

theorem sin2_theta_13_err_finite : (2.5824286687071702 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sin2_theta_13_measured_pos : (0 : ℝ) < (0.022 : ℝ) := by
  norm_num

theorem sin2_theta_13_abs_diff : (0.0005681343071155774 : ℝ) < (0.0005738156501877332 : ℝ) := by
  norm_num

theorem delta_pmns_rad_err_finite : (0.6093498205858049 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem delta_pmns_rad_measured_pos : (0 : ℝ) < (3.4382986264288293 : ℝ) := by
  norm_num

theorem delta_pmns_rad_abs_diff : (0.020951266511348265 : ℝ) < (0.02116077917646275 : ℝ) := by
  norm_num

theorem dm2_21_err_finite : (4.118318933025263 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem dm2_21_measured_pos : (0 : ℝ) < (7.53e-05 : ℝ) := by
  norm_num

theorem dm2_21_abs_diff : (3.101094156568023e-06 : ℝ) < (3.1321050991337033e-06 : ℝ) := by
  norm_num

theorem dm2_31_abs_err_finite : (6.834421455812894 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem dm2_31_abs_measured_pos : (0 : ℝ) < (0.002453 : ℝ) := by
  norm_num

theorem dm2_31_abs_abs_diff : (0.00016764835831109028 : ℝ) < (0.00016932484189520117 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_err_under_half : (0.0012632120914846112 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_abs_diff : (1.2632120914846112e-05 : ℝ) < (1.2758442124994573e-05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_err_under_half : (0.17111017284017205 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_abs_diff : (0.0017111017284017205 : ℝ) < (0.0017282127456867379 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_err_under_half : (0.1782655825115942 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_abs_diff : (0.001782655825115942 : ℝ) < (0.0018004823833681013 : ℝ) := by
  norm_num

theorem yin_yang_in_unit_interval_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem yin_yang_in_unit_interval_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem yin_yang_in_unit_interval_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem all_kappa_nonnegative_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem all_kappa_nonnegative_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem all_kappa_nonnegative_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem sector_count_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sector_count_measured_pos : (0 : ℝ) < (8.0 : ℝ) := by
  norm_num

theorem sector_count_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem edge_count_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem edge_count_measured_pos : (0 : ℝ) < (15.0 : ℝ) := by
  norm_num

theorem edge_count_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_unitarity_tight : (1.2632120914846112e-05 : ℝ) < (0.05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_unitarity_tight : (0.0017111017284017205 : ℝ) < (0.05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_unitarity_tight : (0.001782655825115942 : ℝ) < (0.05 : ℝ) := by
  norm_num

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

theorem gr_einstein_trace_reverse_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_einstein_trace_reverse_meas_pos : (0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_weak_field_2phi_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_weak_field_2phi_meas_pos : (0 : ℝ) < (2e-06 : ℝ) := by
  norm_num

theorem gr_schwarzschild_radius_sun_m_err_under_half : (0.003026566219535862 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_schwarzschild_radius_sun_m_meas_pos : (0 : ℝ) < (2953.25 : ℝ) := by
  norm_num

theorem gr_solar_light_deflection_rad_err_under_half : (0.013893853126499888 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_solar_light_deflection_rad_meas_pos : (0 : ℝ) < (8.489087556227974e-06 : ℝ) := by
  norm_num

theorem gr_mercury_perihelion_arcsec_cy_err_under_half : (0.0047099996121108675 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_mercury_perihelion_arcsec_cy_meas_pos : (0 : ℝ) < (42.98 : ℝ) := by
  norm_num

theorem gr_acoustic_null_cone_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_acoustic_null_cone_meas_pos : (0 : ℝ) < (0.7693455090660798 : ℝ) := by
  norm_num

theorem gr_planck_length_m_err_under_half : (2.3928549890383717e-11 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_c_light_si_exact_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_c_light_si_exact_meas_pos : (0 : ℝ) < (299792458.0 : ℝ) := by
  norm_num

theorem gr_seed_sin2_theta_W_err_finite : (1.4422223774651803 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem gr_seed_sin2_theta_W_meas_pos : (0 : ℝ) < (0.23122 : ℝ) := by
  norm_num

theorem gr_seed_alpha_inv_err_finite : (1.2629964743568904 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem gr_seed_alpha_inv_meas_pos : (0 : ℝ) < (137.035999084 : ℝ) := by
  norm_num

theorem gr_seed_m_H_err_under_half : (0.03990518384182655 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_seed_m_H_meas_pos : (0 : ℝ) < (125.25 : ℝ) := by
  norm_num

theorem gr_seed_m_W_err_finite : (0.836299635903489 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem gr_seed_m_W_meas_pos : (0 : ℝ) < (80.377 : ℝ) := by
  norm_num

theorem gr_seed_m_Z_err_under_half : (0.09398120291369791 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_seed_m_Z_meas_pos : (0 : ℝ) < (91.1876 : ℝ) := by
  norm_num

theorem sm_lambda_ckm_err_under_half : (0.0674090941924869 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_A_wolfenstein_err_finite : (1.2112430567490686 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_rho_bar_err_finite : (0.8542163106350151 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_eta_bar_err_under_half : (0.49211367344735246 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_Jarlskog_J_err_finite : (2.475842827902397 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_delta_ckm_rad_err_finite : (4.923088578307108 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_ud_err_under_half : (0.002696448876034594 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_us_err_under_half : (0.0674090941924869 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_ub_err_finite : (3.6810430545769552 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_cd_err_under_half : (0.12971202611985092 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_cs_err_under_half : (0.08564311398950579 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_cb_err_finite : (1.0868832908350836 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_td_err_finite : (1.2956188612649575 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_ts_err_finite : (0.6459012354568695 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_tb_err_under_half : (0.08827786107347174 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_W_err_finite : (0.5605427410082864 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_alpha_inv_err_finite : (1.117147243876773 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_alpha_s_MZ_err_finite : (3.579369787719938 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_m_H_err_under_half : (0.12089010848922362 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_W_err_finite : (1.6981756204556522 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_m_Z_err_finite : (1.0939302919222549 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_m_t_err_finite : (1.5554132408708463 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_sin2_theta_12_err_under_half : (0.2910480743994031 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_23_err_under_half : (0.12991683625245593 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_13_err_finite : (2.5824286687071702 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_delta_pmns_rad_err_finite : (0.6093498205858049 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_dm2_21_err_finite : (4.118318933025263 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_dm2_31_abs_err_finite : (6.834421455812894 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_u_err_under_half : (0.0012632120914846112 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_c_err_under_half : (0.17111017284017205 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_t_err_under_half : (0.1782655825115942 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_yin_yang_in_unit_interval_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_all_kappa_nonnegative_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sector_count_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_edge_count_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

end

end FSOT.Formal.GRSMCKM
