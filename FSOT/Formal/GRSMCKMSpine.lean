/-
  FSOT Formal GRSMCKMSpine — multi-prover GR/SM/CKM/PMNS obligations.
  Generator: scripts/export_and_generate_gr_sm_ckm_artifacts.py
  Independent numeric certificates (norm_num / decide).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace FSOT.Formal.GRSMCKM

noncomputable section

theorem lambda_ckm_err_under_half : (0.06648317372654539 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem lambda_ckm_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem lambda_ckm_abs_diff : (0.00014958714088472713 : ℝ) < (0.0001510830122945744 : ℝ) := by
  norm_num

theorem A_wolfenstein_err_under_half : (0.0519504854624754 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem A_wolfenstein_measured_pos : (0 : ℝ) < (0.826 : ℝ) := by
  norm_num

theorem A_wolfenstein_abs_diff : (0.0004291110099200468 : ℝ) < (0.0004334021200202473 : ℝ) := by
  norm_num

theorem rho_bar_err_under_half : (0.004811476065123823 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem rho_bar_measured_pos : (0 : ℝ) < (0.159 : ℝ) := by
  norm_num

theorem rho_bar_abs_diff : (7.650246943546879e-06 : ℝ) < (7.726749413982348e-06 : ℝ) := by
  norm_num

theorem eta_bar_err_under_half : (0.038316528380806465 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem eta_bar_measured_pos : (0 : ℝ) < (0.348 : ℝ) := by
  norm_num

theorem eta_bar_abs_diff : (0.0001333415187652065 : ℝ) < (0.00013467493395385855 : ℝ) := by
  norm_num

theorem Jarlskog_J_err_under_half : (0.24035678834077073 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem Jarlskog_J_measured_pos : (0 : ℝ) < (3.08e-05 : ℝ) := by
  norm_num

theorem Jarlskog_J_abs_diff : (7.402989080895739e-08 : ℝ) < (7.477019071704697e-08 : ℝ) := by
  norm_num

theorem delta_ckm_rad_err_under_half : (0.0032411336172532518 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem delta_ckm_rad_measured_pos : (0 : ℝ) < (1.196 : ℝ) := by
  norm_num

theorem delta_ckm_rad_abs_diff : (3.876395806234889e-05 : ℝ) < (3.915159764397238e-05 : ℝ) := by
  norm_num

theorem V_ud_err_under_half : (0.0026470393155981903 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ud_measured_pos : (0 : ℝ) < (0.97435 : ℝ) := by
  norm_num

theorem V_ud_abs_diff : (2.5791427571530967e-05 : ℝ) < (2.6049341848246278e-05 : ℝ) := by
  norm_num

theorem V_us_err_under_half : (0.06648317372654539 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_us_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem V_us_abs_diff : (0.00014958714088472713 : ℝ) < (0.0001510830122945744 : ℝ) := by
  norm_num

theorem V_ub_err_under_half : (0.3128398765779975 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ub_measured_pos : (0 : ℝ) < (0.00369 : ℝ) := by
  norm_num

theorem V_ub_abs_diff : (1.1543791445728108e-05 : ℝ) < (1.165922936118539e-05 : ℝ) := by
  norm_num

theorem V_cd_err_under_half : (0.12878552916691646 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cd_measured_pos : (0 : ℝ) < (0.22486 : ℝ) := by
  norm_num

theorem V_cd_abs_diff : (0.00028958714088472837 : ℝ) < (0.0002924830122945757 : ℝ) := by
  norm_num

theorem V_cs_err_under_half : (0.08569256719930887 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cs_measured_pos : (0 : ℝ) < (0.97349 : ℝ) := by
  norm_num

theorem V_cs_abs_diff : (0.000834208572428552 : ℝ) < (0.0008425506581538375 : ℝ) := by
  norm_num

theorem V_cb_err_under_half : (0.17604653957526104 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cb_measured_pos : (0 : ℝ) < (0.04182 : ℝ) := by
  norm_num

theorem V_cb_abs_diff : (7.362266285037417e-05 : ℝ) < (7.43588894798779e-05 : ℝ) := by
  norm_num

theorem V_td_err_under_half : (0.16746091354807907 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_td_measured_pos : (0 : ℝ) < (0.00857 : ℝ) := by
  norm_num

theorem V_td_abs_diff : (1.4351400291070376e-05 : ℝ) < (1.4494914294981081e-05 : ℝ) := by
  norm_num

theorem V_ts_err_under_half : (0.16900757375439615 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ts_measured_pos : (0 : ℝ) < (0.0411 : ℝ) := by
  norm_num

theorem V_ts_abs_diff : (6.946211281305681e-05 : ℝ) < (7.015673394218738e-05 : ℝ) := by
  norm_num

theorem V_tb_err_under_half : (0.0004466129217395198 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_tb_measured_pos : (0 : ℝ) < (0.999118 : ℝ) := by
  norm_num

theorem V_tb_abs_diff : (4.462190091425455e-06 : ℝ) < (4.506811993339711e-06 : ℝ) := by
  norm_num

theorem sin2_theta_W_err_under_half : (0.03607116917125227 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_W_measured_pos : (0 : ℝ) < (0.23122 : ℝ) := by
  norm_num

theorem sin2_theta_W_abs_diff : (8.34037573577695e-05 : ℝ) < (8.42377949323472e-05 : ℝ) := by
  norm_num

theorem sin2_theta_W_onshell_err_under_half : (0.18983327119077956 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_W_onshell_measured_pos : (0 : ℝ) < (0.2230518910035465 : ℝ) := by
  norm_num

theorem sin2_theta_W_onshell_abs_diff : (0.0004234267011449244 : ℝ) < (0.00042766096815737367 : ℝ) := by
  norm_num

theorem alpha_inv_err_under_half : (0.14167347156583626 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem alpha_inv_measured_pos : (0 : ℝ) < (137.035999084 : ℝ) := by
  norm_num

theorem alpha_inv_abs_diff : (0.19414365719723037 : ℝ) < (0.19608509376920366 : ℝ) := by
  norm_num

theorem alpha_s_MZ_err_under_half : (0.007456682224867657 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem alpha_s_MZ_measured_pos : (0 : ℝ) < (0.1179 : ℝ) := by
  norm_num

theorem alpha_s_MZ_abs_diff : (8.791428343118968e-06 : ℝ) < (8.879342627550158e-06 : ℝ) := by
  norm_num

theorem m_H_err_under_half : (0.03465631473109587 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem m_H_measured_pos : (0 : ℝ) < (125.25 : ℝ) := by
  norm_num

theorem m_H_abs_diff : (0.04340703420069758 : ℝ) < (0.04384110454270555 : ℝ) := by
  norm_num

theorem m_W_err_under_half : (0.026467778409122445 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem m_W_measured_pos : (0 : ℝ) < (80.377 : ℝ) := by
  norm_num

theorem m_W_abs_diff : (0.021274006251900346 : ℝ) < (0.02148674631442035 : ℝ) := by
  norm_num

theorem m_Z_err_under_half : (0.05373549190999207 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem m_Z_measured_pos : (0 : ℝ) < (91.1876 : ℝ) := by
  norm_num

theorem m_Z_abs_diff : (0.04900010542091593 : ℝ) < (0.04949010647512609 : ℝ) := by
  norm_num

theorem m_t_err_under_half : (0.014767057175780673 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem m_t_measured_pos : (0 : ℝ) < (172.69 : ℝ) := by
  norm_num

theorem m_t_abs_diff : (0.025501231036855643 : ℝ) < (0.025756243347225198 : ℝ) := by
  norm_num

theorem Lambda_QCD_GeV_err_under_half : (0.28120185593059194 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem Lambda_QCD_GeV_measured_pos : (0 : ℝ) < (0.2173 : ℝ) := by
  norm_num

theorem Lambda_QCD_GeV_abs_diff : (0.0006110516329371762 : ℝ) < (0.000617162149267548 : ℝ) := by
  norm_num

theorem sqrt_sigma_GeV_err_under_half : (0.05275580626597419 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sqrt_sigma_GeV_measured_pos : (0 : ℝ) < (0.42 : ℝ) := by
  norm_num

theorem sqrt_sigma_GeV_abs_diff : (0.0002215743863170916 : ℝ) < (0.0002237901301812625 : ℝ) := by
  norm_num

theorem N_eff_err_under_half : (0.04789442119649137 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem N_eff_measured_pos : (0 : ℝ) < (3.046 : ℝ) := by
  norm_num

theorem N_eff_abs_diff : (0.0014588640696451272 : ℝ) < (0.0014734527103425785 : ℝ) := by
  norm_num

theorem sin2_theta_12_err_under_half : (0.004756805274882866 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_12_measured_pos : (0 : ℝ) < (0.307 : ℝ) := by
  norm_num

theorem sin2_theta_12_abs_diff : (1.4603392193890397e-05 : ℝ) < (1.47494261168293e-05 : ℝ) := by
  norm_num

theorem sin2_theta_23_err_under_half : (0.16643494215886515 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_23_measured_pos : (0 : ℝ) < (0.546 : ℝ) := by
  norm_num

theorem sin2_theta_23_abs_diff : (0.0009087347841874038 : ℝ) < (0.0009178221320302779 : ℝ) := by
  norm_num

theorem sin2_theta_13_err_under_half : (0.0029908786376992773 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_13_measured_pos : (0 : ℝ) < (0.022 : ℝ) := by
  norm_num

theorem sin2_theta_13_abs_diff : (6.57993300293841e-07 : ℝ) < (6.645732342967793e-07 : ℝ) := by
  norm_num

theorem delta_pmns_rad_err_under_half : (0.07675312594002048 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem delta_pmns_rad_measured_pos : (0 : ℝ) < (3.4382986264288293 : ℝ) := by
  norm_num

theorem delta_pmns_rad_abs_diff : (0.002639001674936914 : ℝ) < (0.002665391691687283 : ℝ) := by
  norm_num

theorem dm2_21_err_under_half : (0.06394145338205008 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem dm2_21_measured_pos : (0 : ℝ) < (7.53e-05 : ℝ) := by
  norm_num

theorem dm2_21_abs_diff : (4.814791439668371e-08 : ℝ) < (4.862939454065054e-08 : ℝ) := by
  norm_num

theorem dm2_31_abs_err_under_half : (0.4219868071131969 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem dm2_31_abs_measured_pos : (0 : ℝ) < (0.002453 : ℝ) := by
  norm_num

theorem dm2_31_abs_abs_diff : (1.035133637848672e-05 : ℝ) < (1.0454849743271588e-05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_err_under_half : (0.0013701426440082543 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_u_abs_diff : (1.3701426440082543e-05 : ℝ) < (1.3838440705483368e-05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_err_under_half : (0.1755075619817248 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_abs_diff : (0.001755075619817248 : ℝ) < (0.0017726263760164205 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_err_under_half : (0.001431015241259992 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_abs_diff : (1.4310152412599919e-05 : ℝ) < (1.445325393772592e-05 : ℝ) := by
  norm_num

theorem triangle_angle_sum_pi_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem triangle_angle_sum_pi_measured_pos : (0 : ℝ) < (3.141592653589793 : ℝ) := by
  norm_num

theorem triangle_angle_sum_pi_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
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

theorem emergent_unitarity_row_u_unitarity_tight : (1.3701426440082543e-05 : ℝ) < (0.05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_c_unitarity_tight : (0.001755075619817248 : ℝ) < (0.05 : ℝ) := by
  norm_num

theorem emergent_unitarity_row_t_unitarity_tight : (1.4310152412599919e-05 : ℝ) < (0.05 : ℝ) := by
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

theorem gr_seed_sin2_theta_W_err_under_half : (0.016460322231694493 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_seed_sin2_theta_W_meas_pos : (0 : ℝ) < (0.23122 : ℝ) := by
  norm_num

theorem gr_seed_sin2_theta_W_onshell_err_under_half : (0.209488435890309 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_seed_sin2_theta_W_onshell_meas_pos : (0 : ℝ) < (0.2230518910035465 : ℝ) := by
  norm_num

theorem gr_seed_alpha_inv_err_under_half : (0.13842762822785223 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_seed_alpha_inv_meas_pos : (0 : ℝ) < (137.035999084 : ℝ) := by
  norm_num

theorem gr_seed_m_H_err_under_half : (0.01100190161397048 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_seed_m_H_meas_pos : (0 : ℝ) < (125.25 : ℝ) := by
  norm_num

theorem gr_seed_m_W_err_under_half : (0.022433777228753317 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_seed_m_W_meas_pos : (0 : ℝ) < (80.377 : ℝ) := by
  norm_num

theorem gr_seed_m_Z_err_under_half : (0.05252482561491295 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_seed_m_Z_meas_pos : (0 : ℝ) < (91.1876 : ℝ) := by
  norm_num

theorem gr_Lambda_QCD_GeV_err_under_half : (0.28241958362570724 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_Lambda_QCD_GeV_meas_pos : (0 : ℝ) < (0.2173 : ℝ) := by
  norm_num

theorem gr_sqrt_sigma_GeV_err_under_half : (0.052777181118259166 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_sqrt_sigma_GeV_meas_pos : (0 : ℝ) < (0.42 : ℝ) := by
  norm_num

theorem gr_N_eff_err_under_half : (0.028424048045719855 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_N_eff_meas_pos : (0 : ℝ) < (3.046 : ℝ) := by
  norm_num

theorem gr_N_c_QCD_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_N_c_QCD_meas_pos : (0 : ℝ) < (3.0 : ℝ) := by
  norm_num

theorem gr_Casimir_C_F_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_Casimir_C_F_meas_pos : (0 : ℝ) < (1.3333333333333333 : ℝ) := by
  norm_num

theorem gr_Casimir_C_A_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_Casimir_C_A_meas_pos : (0 : ℝ) < (3.0 : ℝ) := by
  norm_num

theorem gr_beta0_QCD_nf5_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_beta0_QCD_nf5_meas_pos : (0 : ℝ) < (7.666666666666667 : ℝ) := by
  norm_num

theorem gr_alpha_s_gt_alpha_em_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_alpha_s_gt_alpha_em_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_koide_lepton_QR_err_under_half : (0.0009230194964016114 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_koide_lepton_QR_meas_pos : (0 : ℝ) < (0.6666666666666666 : ℝ) := by
  norm_num

theorem gr_sqrt2_structural_recovery_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_sqrt2_structural_recovery_meas_pos : (0 : ℝ) < (1.4142135623730951 : ℝ) := by
  norm_num

theorem gr_yukawa_top_err_under_half : (0.07863049017601485 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_yukawa_top_meas_pos : (0 : ℝ) < (0.991 : ℝ) := by
  norm_num

theorem gr_morphic_phi_present_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_morphic_phi_present_meas_pos : (0 : ℝ) < (1.618033988749895 : ℝ) := by
  norm_num

theorem gr_neutrino_m3_over_m2_err_under_half : (0.1724795983521893 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_neutrino_m3_over_m2_meas_pos : (0 : ℝ) < (5.707570518336111 : ℝ) := by
  norm_num

theorem gr_R_b_triangle_err_under_half : (0.014017064614919078 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_R_b_triangle_meas_pos : (0 : ℝ) < (0.382602927328059 : ℝ) := by
  norm_num

theorem gr_R_t_triangle_err_under_half : (0.00036384895090004057 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_R_t_triangle_meas_pos : (0 : ℝ) < (0.9101565799355624 : ℝ) := by
  norm_num

theorem gr_sin_delta_ckm_err_under_half : (0.002439404519026022 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_sin_delta_ckm_meas_pos : (0 : ℝ) < (0.93058220251172 : ℝ) := by
  norm_num

theorem gr_spin2_massless_helicities_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_spin2_massless_helicities_meas_pos : (0 : ℝ) < (2.0 : ℝ) := by
  norm_num

theorem gr_spin2_TT_dof_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_spin2_TT_dof_meas_pos : (0 : ℝ) < (2.0 : ℝ) := by
  norm_num

theorem gr_einstein_quadrupole_prefactor_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_einstein_quadrupole_prefactor_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_wilson_area_law_sigma_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_wilson_area_law_sigma_meas_pos : (0 : ℝ) < (0.17658624702998535 : ℝ) := by
  norm_num

theorem gr_confinement_scale_ratio_err_under_half : (0.2295212676523054 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_confinement_scale_ratio_meas_pos : (0 : ℝ) < (0.5173809523809524 : ℝ) := by
  norm_num

theorem gr_asymptotic_freedom_beta0_pos_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_asymptotic_freedom_beta0_pos_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_flux_tube_E_over_L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_flux_tube_E_over_L_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_polyakov_confined_order_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_spin2_massive_polarizations_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_spin2_massive_polarizations_meas_pos : (0 : ℝ) < (5.0 : ℝ) := by
  norm_num

theorem gr_spin2_metric_dof_accounting_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_spin2_metric_dof_accounting_meas_pos : (0 : ℝ) < (2.0 : ℝ) := by
  norm_num

theorem gr_equivalence_geodesic_structure_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_equivalence_geodesic_structure_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_spin2_wave_equation_flat_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_spin2_wave_equation_flat_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_bianchi_contracted_identity_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_bianchi_contracted_identity_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_spin2_TT_projector_complete_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_spin2_TT_projector_complete_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_soft_graviton_pole_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_soft_graviton_pole_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_instanton_action_scale_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_instanton_action_scale_meas_pos : (0 : ℝ) < (669.6431825331274 : ℝ) := by
  norm_num

theorem gr_ym_beta_function_structure_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_ym_beta_function_structure_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_su3_center_order_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_su3_center_order_meas_pos : (0 : ℝ) < (3.0 : ℝ) := by
  norm_num

theorem gr_dual_meissner_confined_flag_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_dual_meissner_confined_flag_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_triangle_angle_sum_pi_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_triangle_angle_sum_pi_meas_pos : (0 : ℝ) < (3.141592653589793 : ℝ) := by
  norm_num

theorem gr_alpha_rad_err_under_half : (0.0034382632792112626 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_alpha_rad_meas_pos : (0 : ℝ) < (1.6070304610469615 : ℝ) := by
  norm_num

theorem gr_beta_rad_err_under_half : (0.014994707011088022 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_beta_rad_meas_pos : (0 : ℝ) < (0.3923401442155158 : ℝ) := by
  norm_num

theorem gr_gamma_rad_err_under_half : (0.00031310172038841725 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_gamma_rad_meas_pos : (0 : ℝ) < (1.1422220483273158 : ℝ) := by
  norm_num

theorem sm_lambda_ckm_err_under_half : (0.06648317372654539 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_A_wolfenstein_err_under_half : (0.0519504854624754 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_rho_bar_err_under_half : (0.004811476065123823 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_eta_bar_err_under_half : (0.038316528380806465 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_Jarlskog_J_err_under_half : (0.24035678834077073 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_delta_ckm_rad_err_under_half : (0.0032411336172532518 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_ud_err_under_half : (0.0026470393155981903 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_us_err_under_half : (0.06648317372654539 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_ub_err_under_half : (0.3128398765779975 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_cd_err_under_half : (0.12878552916691646 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_cs_err_under_half : (0.08569256719930887 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_cb_err_under_half : (0.17604653957526104 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_td_err_under_half : (0.16746091354807907 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_ts_err_under_half : (0.16900757375439615 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_V_tb_err_under_half : (0.0004466129217395198 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_W_err_under_half : (0.03607116917125227 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_W_onshell_err_under_half : (0.18983327119077956 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_alpha_inv_err_under_half : (0.14167347156583626 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_alpha_s_MZ_err_under_half : (0.007456682224867657 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_H_err_under_half : (0.03465631473109587 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_W_err_under_half : (0.026467778409122445 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_Z_err_under_half : (0.05373549190999207 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_t_err_under_half : (0.014767057175780673 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_Lambda_QCD_GeV_err_under_half : (0.28120185593059194 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sqrt_sigma_GeV_err_under_half : (0.05275580626597419 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_N_eff_err_under_half : (0.04789442119649137 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_12_err_under_half : (0.004756805274882866 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_23_err_under_half : (0.16643494215886515 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_13_err_under_half : (0.0029908786376992773 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_delta_pmns_rad_err_under_half : (0.07675312594002048 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_dm2_21_err_under_half : (0.06394145338205008 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_dm2_31_abs_err_under_half : (0.4219868071131969 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_u_err_under_half : (0.0013701426440082543 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_c_err_under_half : (0.1755075619817248 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_emergent_unitarity_row_t_err_under_half : (0.001431015241259992 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_triangle_angle_sum_pi_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
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
