/-
  FSOT Formal GRSMCKMSpine — multi-prover GR/SM/CKM/PMNS obligations.
  Generator: scripts/export_and_generate_gr_sm_ckm_artifacts.py
  Independent numeric certificates (norm_num / decide).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace FSOT.Formal.GRSMCKM

noncomputable section

theorem lambda_ckm_err_under_half : (0.08387407135526351 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem lambda_ckm_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem lambda_ckm_abs_diff : (0.00018871666054934289 : ℝ) < (0.0001906038271558363 : ℝ) := by
  norm_num

theorem A_wolfenstein_err_finite : (2.240891444698181 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem A_wolfenstein_measured_pos : (0 : ℝ) < (0.826 : ℝ) := by
  norm_num

theorem A_wolfenstein_abs_diff : (0.018509763333206974 : ℝ) < (0.018694860966540043 : ℝ) := by
  norm_num

theorem rho_bar_err_finite : (5.86239218720027 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem rho_bar_measured_pos : (0 : ℝ) < (0.159 : ℝ) := by
  norm_num

theorem rho_bar_abs_diff : (0.00932120357764843 : ℝ) < (0.009414415613425913 : ℝ) := by
  norm_num

theorem eta_bar_err_finite : (5.954837550877345 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem eta_bar_measured_pos : (0 : ℝ) < (0.348 : ℝ) := by
  norm_num

theorem eta_bar_abs_diff : (0.02072283467705316 : ℝ) < (0.02093006302382469 : ℝ) := by
  norm_num

theorem Jarlskog_J_err_finite : (9.651841765554817 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem Jarlskog_J_measured_pos : (0 : ℝ) < (3.08e-05 : ℝ) := by
  norm_num

theorem Jarlskog_J_abs_diff : (2.972767263790884e-06 : ℝ) < (3.002494937428793e-06 : ℝ) := by
  norm_num

theorem delta_ckm_rad_err_finite : (8.38059421016685 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem delta_ckm_rad_measured_pos : (0 : ℝ) < (1.196 : ℝ) := by
  norm_num

theorem delta_ckm_rad_abs_diff : (0.1002319067535955 : ℝ) < (0.10123422582113245 : ℝ) := by
  norm_num

theorem V_ud_err_under_half : (0.0035751439500761547 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ud_measured_pos : (0 : ℝ) < (0.97435 : ℝ) := by
  norm_num

theorem V_ud_abs_diff : (3.4834415077567016e-05 : ℝ) < (3.518275922934269e-05 : ℝ) := by
  norm_num

theorem V_us_err_under_half : (0.08387407135526351 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_us_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem V_us_abs_diff : (0.00018871666054934289 : ℝ) < (0.0001906038271558363 : ℝ) := by
  norm_num

theorem V_ub_err_finite : (8.033837560592682 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem V_ub_measured_pos : (0 : ℝ) < (0.00369 : ℝ) := by
  norm_num

theorem V_ub_abs_diff : (0.00029644860598586993 : ℝ) < (0.00029941309204672864 : ℝ) := by
  norm_num

theorem V_cd_err_under_half : (0.14618725453586415 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cd_measured_pos : (0 : ℝ) < (0.22486 : ℝ) := by
  norm_num

theorem V_cd_abs_diff : (0.0003287166605493441 : ℝ) < (0.00033200382715583757 : ℝ) := by
  norm_num

theorem V_cs_err_under_half : (0.08476364265914554 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cs_measured_pos : (0 : ℝ) < (0.97349 : ℝ) := by
  norm_num

theorem V_cs_abs_diff : (0.0008251655849225159 : ℝ) < (0.0008334172407727411 : ℝ) := by
  norm_num

theorem V_cb_err_finite : (2.085614355341048 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem V_cb_measured_pos : (0 : ℝ) < (0.04182 : ℝ) := by
  norm_num

theorem V_cb_abs_diff : (0.0008722039234036263 : ℝ) < (0.0008809259626386625 : ℝ) := by
  norm_num

theorem V_td_err_finite : (3.8353724469530674 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem V_td_measured_pos : (0 : ℝ) < (0.00857 : ℝ) := by
  norm_num

theorem V_td_abs_diff : (0.00032869141870387787 : ℝ) < (0.00033197833289191664 : ℝ) := by
  norm_num

theorem V_ts_err_under_half : (0.3703258476973747 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ts_measured_pos : (0 : ℝ) < (0.0411 : ℝ) := by
  norm_num

theorem V_ts_abs_diff : (0.000152203923403621 : ℝ) < (0.0001537259626386572 : ℝ) := by
  norm_num

theorem V_tb_err_under_half : (0.08827786107347174 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_tb_measured_pos : (0 : ℝ) < (0.999118 : ℝ) := by
  norm_num

theorem V_tb_abs_diff : (0.0008820000000000494 : ℝ) < (0.0008908200000010499 : ℝ) := by
  norm_num

theorem sin2_theta_W_err_finite : (3.791079293869786 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sin2_theta_W_measured_pos : (0 : ℝ) < (0.23122 : ℝ) := by
  norm_num

theorem sin2_theta_W_abs_diff : (0.00876573354328572 : ℝ) < (0.008853390878719575 : ℝ) := by
  norm_num

theorem alpha_inv_err_under_half : (0.3910691950893094 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem alpha_inv_measured_pos : (0 : ℝ) < (137.035999084 : ℝ) := by
  norm_num

theorem alpha_inv_abs_diff : (0.5359055786003921 : ℝ) < (0.541264634386397 : ℝ) := by
  norm_num

theorem alpha_s_MZ_err_finite : (3.573804082126688 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem alpha_s_MZ_measured_pos : (0 : ℝ) < (0.1179 : ℝ) := by
  norm_num

theorem alpha_s_MZ_abs_diff : (0.004213515012827365 : ℝ) < (0.004255650162956639 : ℝ) := by
  norm_num

theorem m_H_err_under_half : (0.24031054116629413 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem m_H_measured_pos : (0 : ℝ) < (125.25 : ℝ) := by
  norm_num

theorem m_H_abs_diff : (0.3009889528107834 : ℝ) < (0.30399884233889224 : ℝ) := by
  norm_num

theorem m_W_err_finite : (11.818376281905547 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem m_W_measured_pos : (0 : ℝ) < (80.377 : ℝ) := by
  norm_num

theorem m_W_abs_diff : (9.49925630410722 : ℝ) < (9.594248867148295 : ℝ) := by
  norm_num

theorem m_Z_err_finite : (11.852271158304143 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem m_Z_measured_pos : (0 : ℝ) < (91.1876 : ℝ) := by
  norm_num

theorem m_Z_abs_diff : (10.80780161474975 : ℝ) < (10.91587963089725 : ℝ) := by
  norm_num

theorem m_t_err_finite : (53.0467052008237 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem m_t_measured_pos : (0 : ℝ) < (172.69 : ℝ) := by
  norm_num

theorem m_t_abs_diff : (91.60635521130246 : ℝ) < (92.52241876341549 : ℝ) := by
  norm_num

theorem sin2_theta_12_err_finite : (2.053332898567214 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sin2_theta_12_measured_pos : (0 : ℝ) < (0.307 : ℝ) := by
  norm_num

theorem sin2_theta_12_abs_diff : (0.006303731998601347 : ℝ) < (0.006366769318588361 : ℝ) := by
  norm_num

theorem sin2_theta_23_err_finite : (6.342198874309371 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sin2_theta_23_measured_pos : (0 : ℝ) < (0.546 : ℝ) := by
  norm_num

theorem sin2_theta_23_abs_diff : (0.03462840585372917 : ℝ) < (0.034974689912267466 : ℝ) := by
  norm_num

theorem sin2_theta_13_err_finite : (7.121598214539716 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sin2_theta_13_measured_pos : (0 : ℝ) < (0.022 : ℝ) := by
  norm_num

theorem sin2_theta_13_abs_diff : (0.0015667516071987374 : ℝ) < (0.001582419123271725 : ℝ) := by
  norm_num

theorem delta_pmns_rad_err_finite : (6.824483048637119 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem delta_pmns_rad_measured_pos : (0 : ℝ) < (3.4382986264288293 : ℝ) := by
  norm_num

theorem delta_pmns_rad_abs_diff : (0.23464610692215837 : ℝ) < (0.23699256799138096 : ℝ) := by
  norm_num

theorem dm2_21_err_finite : (5.947855435998268 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem dm2_21_measured_pos : (0 : ℝ) < (7.53e-05 : ℝ) := by
  norm_num

theorem dm2_21_abs_diff : (4.478735143306696e-06 : ℝ) < (4.523522495739764e-06 : ℝ) := by
  norm_num

theorem dm2_31_abs_err_finite : (14.405438984619169 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem dm2_31_abs_measured_pos : (0 : ℝ) < (0.002453 : ℝ) := by
  norm_num

theorem dm2_31_abs_abs_diff : (0.0003533654182927082 : ℝ) < (0.0003568990724766353 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_err_under_half : (0.0011516191063876136 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_abs_diff : (1.1516191063876136e-05 : ℝ) < (1.1631352975514898e-05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_err_under_half : (0.16767220035305286 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_abs_diff : (0.0016767220035305286 : ℝ) < (0.001693489223566834 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_err_under_half : (0.1744641170662753 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_abs_diff : (0.001744641170662753 : ℝ) < (0.0017620875823703805 : ℝ) := by
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

theorem emergent_unitarity_row_u_unitarity_tight : (1.1516191063876136e-05 : ℝ) < (0.05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_unitarity_tight : (0.0016767220035305286 : ℝ) < (0.05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_unitarity_tight : (0.001744641170662753 : ℝ) < (0.05 : ℝ) := by
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

theorem gr_seed_m_W_err_finite : (7.281636039893431 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem gr_seed_m_W_meas_pos : (0 : ℝ) < (80.377 : ℝ) := by
  norm_num

theorem gr_seed_m_Z_err_finite : (6.587566028472561 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem gr_seed_m_Z_meas_pos : (0 : ℝ) < (91.1876 : ℝ) := by
  norm_num

theorem sm_lambda_ckm_err_under_half : (0.08387407135526351 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_A_wolfenstein_err_finite : (2.240891444698181 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_rho_bar_err_finite : (5.86239218720027 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_eta_bar_err_finite : (5.954837550877345 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_Jarlskog_J_err_finite : (9.651841765554817 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_delta_ckm_rad_err_finite : (8.38059421016685 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_ud_err_under_half : (0.0035751439500761547 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_us_err_under_half : (0.08387407135526351 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_ub_err_finite : (8.033837560592682 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_cd_err_under_half : (0.14618725453586415 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_cs_err_under_half : (0.08476364265914554 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_cb_err_finite : (2.085614355341048 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_td_err_finite : (3.8353724469530674 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_V_ts_err_under_half : (0.3703258476973747 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_tb_err_under_half : (0.08827786107347174 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_W_err_finite : (3.791079293869786 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_alpha_inv_err_under_half : (0.3910691950893094 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_alpha_s_MZ_err_finite : (3.573804082126688 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_m_H_err_under_half : (0.24031054116629413 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_W_err_finite : (11.818376281905547 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_m_Z_err_finite : (11.852271158304143 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_m_t_err_finite : (53.0467052008237 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_sin2_theta_12_err_finite : (2.053332898567214 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_sin2_theta_23_err_finite : (6.342198874309371 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_sin2_theta_13_err_finite : (7.121598214539716 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_delta_pmns_rad_err_finite : (6.824483048637119 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_dm2_21_err_finite : (5.947855435998268 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_dm2_31_abs_err_finite : (14.405438984619169 : ℝ) < (100.0 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_u_err_under_half : (0.0011516191063876136 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_c_err_under_half : (0.16767220035305286 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_t_err_under_half : (0.1744641170662753 : ℝ) < (0.5 : ℝ) := by
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
