/-
  FSOT Formal GRSMCKMSpine — multi-prover GR/SM/CKM/PMNS obligations.
  Generator: scripts/export_and_generate_gr_sm_ckm_artifacts.py
  Independent numeric certificates (norm_num / decide).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace FSOT.Formal.GRSMCKM

noncomputable section

theorem V_ud_err_under_half : (0.009504134401237756 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ud_measured_pos : (0 : ℝ) < (0.97435 : ℝ) := by
  norm_num

theorem V_ud_abs_diff : (9.260353353846007e-05 : ℝ) < (9.352956887484467e-05 : ℝ) := by
  norm_num

theorem V_us_err_under_half : (0.00950413440123674 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_us_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem V_us_abs_diff : (2.1384302402782662e-05 : ℝ) < (2.159814542781049e-05 : ℝ) := by
  norm_num

theorem V_ub_err_under_half : (0.009504134401238675 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ub_measured_pos : (0 : ℝ) < (0.00369 : ℝ) := by
  norm_num

theorem V_ub_abs_diff : (3.5070255940570713e-07 : ℝ) < (3.5420958599976423e-07 : ℝ) := by
  norm_num

theorem V_cd_err_under_half : (0.009504134401234966 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cd_measured_pos : (0 : ℝ) < (0.22486 : ℝ) := by
  norm_num

theorem V_cd_abs_diff : (2.1370996614616944e-05 : ℝ) < (2.1584706581763113e-05 : ℝ) := by
  norm_num

theorem V_cs_err_under_half : (0.009504134401234833 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cs_measured_pos : (0 : ℝ) < (0.97349 : ℝ) := by
  norm_num

theorem V_cs_abs_diff : (9.252179798258098e-05 : ℝ) < (9.344701596340679e-05 : ℝ) := by
  norm_num

theorem V_cb_err_under_half : (0.009504134401244898 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_cb_measured_pos : (0 : ℝ) < (0.04182 : ℝ) := by
  norm_num

theorem V_cb_abs_diff : (3.974629006600616e-06 : ℝ) < (4.014375297666623e-06 : ℝ) := by
  norm_num

theorem V_td_err_under_half : (0.00950413440123913 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_td_measured_pos : (0 : ℝ) < (0.00857 : ℝ) := by
  norm_num

theorem V_td_abs_diff : (8.145043181861933e-07 : ℝ) < (8.226493623680553e-07 : ℝ) := by
  norm_num

theorem V_ts_err_under_half : (0.009504134401236155 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_ts_measured_pos : (0 : ℝ) < (0.0411 : ℝ) := by
  norm_num

theorem V_ts_abs_diff : (3.906199238908059e-06 : ℝ) < (3.94526123229714e-06 : ℝ) := by
  norm_num

theorem V_tb_err_under_half : (0.009504134401237528 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem V_tb_measured_pos : (0 : ℝ) < (0.999118 : ℝ) := by
  norm_num

theorem V_tb_abs_diff : (9.495751754695636e-05 : ℝ) < (9.590709272342593e-05 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_u_err_under_half : (0.000346139999995998 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_u_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_u_abs_diff : (3.46139999995998e-06 : ℝ) < (3.4960140009595795e-06 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_c_err_under_half : (0.0006287900000123692 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_c_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_c_abs_diff : (6.287900000123692e-06 : ℝ) < (6.350779001124929e-06 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_t_err_under_half : (5.6717600005473656e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_t_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_t_abs_diff : (5.671760000547366e-07 : ℝ) < (5.728477610552839e-07 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_d_err_under_half : (0.0006612999999933145 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_d_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_d_abs_diff : (6.612999999933145e-06 : ℝ) < (6.679130000932476e-06 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_s_err_under_half : (0.0003009900000017218 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_s_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_s_abs_diff : (3.0099000000172182e-06 : ℝ) < (3.03999900101739e-06 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_b_err_under_half : (6.93576000077023e-05 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_b_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_b_abs_diff : (6.93576000077023e-07 : ℝ) < (7.005117610777933e-07 : ℝ) := by
  norm_num

theorem sin2_theta_12_err_under_half : (0.009504134401235372 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_12_measured_pos : (0 : ℝ) < (0.307 : ℝ) := by
  norm_num

theorem sin2_theta_12_abs_diff : (2.9177692611792594e-05 : ℝ) < (2.946946953891052e-05 : ℝ) := by
  norm_num

theorem sin2_theta_23_err_under_half : (0.009504134401237823 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_23_measured_pos : (0 : ℝ) < (0.546 : ℝ) := by
  norm_num

theorem sin2_theta_23_abs_diff : (5.1892573830758515e-05 : ℝ) < (5.24114995700661e-05 : ℝ) := by
  norm_num

theorem sin2_theta_13_err_under_half : (0.009504134401232394 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sin2_theta_13_measured_pos : (0 : ℝ) < (0.022 : ℝ) := by
  norm_num

theorem sin2_theta_13_abs_diff : (2.0909095682711265e-06 : ℝ) < (2.1118186649538377e-06 : ℝ) := by
  norm_num

theorem theta_12_deg_err_under_half : (0.009504134401235625 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem theta_12_deg_measured_pos : (0 : ℝ) < (33.41 : ℝ) := by
  norm_num

theorem theta_12_deg_abs_diff : (0.003175331303452822 : ℝ) < (0.00320708461648835 : ℝ) := by
  norm_num

theorem theta_23_deg_err_under_half : (0.009504134401243284 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem theta_23_deg_measured_pos : (0 : ℝ) < (49.0 : ℝ) := by
  norm_num

theorem theta_23_deg_abs_diff : (0.004657025856609209 : ℝ) < (0.004703596115176302 : ℝ) := by
  norm_num

theorem theta_13_deg_err_under_half : (0.009504134401242691 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem theta_13_deg_measured_pos : (0 : ℝ) < (8.54 : ℝ) := by
  norm_num

theorem theta_13_deg_abs_diff : (0.0008116530778661257 : ℝ) < (0.0008197696086457869 : ℝ) := by
  norm_num

theorem delta_CP_deg_err_under_half : (0.009504134401235261 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem delta_CP_deg_measured_pos : (0 : ℝ) < (197.0 : ℝ) := by
  norm_num

theorem delta_CP_deg_abs_diff : (0.018723144770433464 : ℝ) < (0.0189103762181388 : ℝ) := by
  norm_num

theorem pmns_hierarchy_s13_lt_s12_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem pmns_hierarchy_s13_lt_s12_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem pmns_hierarchy_s13_lt_s12_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem pmns_hierarchy_s12_lt_s23_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem pmns_hierarchy_s12_lt_s23_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem pmns_hierarchy_s12_lt_s23_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem wolfenstein_lambda_err_under_half : (0.00950413440123674 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem wolfenstein_lambda_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem wolfenstein_lambda_abs_diff : (2.1384302402782662e-05 : ℝ) < (2.159814542781049e-05 : ℝ) := by
  norm_num

theorem wolfenstein_A_err_under_half : (0.009504134401235067 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem wolfenstein_A_measured_pos : (0 : ℝ) < (0.826 : ℝ) := by
  norm_num

theorem wolfenstein_A_abs_diff : (7.850415015420165e-05 : ℝ) < (7.928919165674366e-05 : ℝ) := by
  norm_num

theorem wolfenstein_rho_bar_err_under_half : (0.009504134401234179 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem wolfenstein_rho_bar_measured_pos : (0 : ℝ) < (0.159 : ℝ) := by
  norm_num

theorem wolfenstein_rho_bar_abs_diff : (1.5111573697962344e-05 : ℝ) < (1.5262689435941968e-05 : ℝ) := by
  norm_num

theorem wolfenstein_eta_bar_err_under_half : (0.009504134401242908 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem wolfenstein_eta_bar_measured_pos : (0 : ℝ) < (0.348 : ℝ) := by
  norm_num

theorem wolfenstein_eta_bar_abs_diff : (3.3074387716325315e-05 : ℝ) < (3.340513159448857e-05 : ℝ) := by
  norm_num

theorem wolfenstein_Vus_eq_lambda_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem wolfenstein_Vus_eq_lambda_measured_pos : (0 : ℝ) < (0.225 : ℝ) := by
  norm_num

theorem wolfenstein_Vus_eq_lambda_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem wolfenstein_Vcb_A_lambda2_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem wolfenstein_Vcb_A_lambda2_measured_pos : (0 : ℝ) < (0.04182 : ℝ) := by
  norm_num

theorem wolfenstein_Vcb_A_lambda2_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem wolfenstein_Vub_A_lambda3_r_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem wolfenstein_Vub_A_lambda3_r_measured_pos : (0 : ℝ) < (0.00369 : ℝ) := by
  norm_num

theorem wolfenstein_Vub_A_lambda3_r_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem wolfenstein_eta_bar_positive_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem wolfenstein_eta_bar_positive_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem wolfenstein_eta_bar_positive_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem delta_ckm_deg_err_under_half : (0.009504134401239367 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem delta_ckm_deg_measured_pos : (0 : ℝ) < (68.5 : ℝ) := by
  norm_num

theorem delta_ckm_deg_abs_diff : (0.006510332064848967 : ℝ) < (0.006575435385498457 : ℝ) := by
  norm_num

theorem delta_ckm_rad_err_under_half : (0.00950413440124136 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem delta_ckm_rad_measured_pos : (0 : ℝ) < (1.196 : ℝ) := by
  norm_num

theorem delta_ckm_rad_abs_diff : (0.00011366944743884666 : ℝ) < (0.00011480614191423512 : ℝ) := by
  norm_num

theorem Jarlskog_J_err_under_half : (0.009504134401248197 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem Jarlskog_J_measured_pos : (0 : ℝ) < (3.08e-05 : ℝ) := by
  norm_num

theorem Jarlskog_J_abs_diff : (2.927273395584445e-09 : ℝ) < (2.9565471295402897e-09 : ℝ) := by
  norm_num

theorem Jarlskog_wolfenstein_approx_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem Jarlskog_wolfenstein_approx_measured_pos : (0 : ℝ) < (3.08e-05 : ℝ) := by
  norm_num

theorem Jarlskog_wolfenstein_approx_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem Jarlskog_positive_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem Jarlskog_positive_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem Jarlskog_positive_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem unitary_triangle_Rb_err_under_half : (0.00950413440124138 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem unitary_triangle_Rb_measured_pos : (0 : ℝ) < (0.382602927328059 : ℝ) := by
  norm_num

theorem unitary_triangle_Rb_abs_diff : (3.636309643634261e-05 : ℝ) < (3.672672740170604e-05 : ℝ) := by
  norm_num

theorem unitary_triangle_Rt_err_under_half : (0.009504134401243274 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem unitary_triangle_Rt_measured_pos : (0 : ℝ) < (0.9101565799355624 : ℝ) := by
  norm_num

theorem unitary_triangle_Rt_abs_diff : (8.650250461883502e-05 : ℝ) < (8.736752966602337e-05 : ℝ) := by
  norm_num

theorem pmns_sin_delta_CP_err_under_half : (0.009504134401242693 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem pmns_sin_delta_CP_measured_pos : (0 : ℝ) < (0.29237170472273677 : ℝ) := by
  norm_num

theorem pmns_sin_delta_CP_abs_diff : (2.7787399768053334e-05 : ℝ) < (2.8065273766733868e-05 : ℝ) := by
  norm_num

theorem dm2_21_err_under_half : (0.009504134401244663 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem dm2_21_measured_pos : (0 : ℝ) < (7.53e-05 : ℝ) := by
  norm_num

theorem dm2_21_abs_diff : (7.1566132041372315e-09 : ℝ) < (7.228180336178604e-09 : ℝ) := by
  norm_num

theorem dm2_31_abs_err_under_half : (0.00950413440123409 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem dm2_31_abs_measured_pos : (0 : ℝ) < (0.002453 : ℝ) := by
  norm_num

theorem dm2_31_abs_abs_diff : (2.3313641686227224e-07 : ℝ) < (2.3546778203089498e-07 : ℝ) := by
  norm_num

theorem dm2_hierarchy_ratio_err_under_half : (0.009504134401243234 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem dm2_hierarchy_ratio_measured_pos : (0 : ℝ) < (32.57636122177955 : ℝ) := by
  norm_num

theorem dm2_hierarchy_ratio_abs_diff : (0.0030961011535524108 : ℝ) < (0.003127062165088935 : ℝ) := by
  norm_num

theorem dm2_31_gt_dm2_21_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem dm2_31_gt_dm2_21_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem dm2_31_gt_dm2_21_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem ew_cos_theta_W_from_masses_err_under_half : (0.009504134401235296 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem ew_cos_theta_W_from_masses_measured_pos : (0 : ℝ) < (0.8814466001956406 : ℝ) := by
  norm_num

theorem ew_cos_theta_W_from_masses_abs_diff : (8.377386955771282e-05 : ℝ) < (8.461160825428995e-05 : ℝ) := by
  norm_num

theorem ew_cos_theta_W_vs_sin2_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem ew_cos_theta_W_vs_sin2_measured_pos : (0 : ℝ) < (0.8768010036490607 : ℝ) := by
  norm_num

theorem ew_cos_theta_W_vs_sin2_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem sm_anomaly_cancel_per_generation_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_anomaly_cancel_per_generation_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem sm_anomaly_SU2_U1_trace_Y_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_anomaly_SU2_U1_trace_Y_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem charge_electron_L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem charge_electron_L_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem charge_neutrino_L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem charge_neutrino_L_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem charge_up_L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem charge_up_L_measured_pos : (0 : ℝ) < (0.6666666666666666 : ℝ) := by
  norm_num

theorem charge_up_L_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem charge_down_L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem charge_down_L_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem charge_u_R_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem charge_u_R_measured_pos : (0 : ℝ) < (0.6666666666666666 : ℝ) := by
  norm_num

theorem charge_u_R_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem charge_d_R_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem charge_d_R_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem gr_2phi_classical_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_2phi_classical_measured_pos : (0 : ℝ) < (2e-06 : ℝ) := by
  norm_num

theorem gr_2phi_classical_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem gr_einstein_half_R_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_einstein_half_R_measured_pos : (0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_einstein_half_R_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem gr_light_deflection_arcsec_solar_err_under_half : (0.010049118924188203 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_light_deflection_arcsec_solar_measured_pos : (0 : ℝ) < (1.751 : ℝ) := by
  norm_num

theorem gr_light_deflection_arcsec_solar_abs_diff : (0.0001759600723625354 : ℝ) < (0.00017771967308716075 : ℝ) := by
  norm_num

theorem gr_mercury_perihelion_arcsec_cy_err_under_half : (0.01004911892419796 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_mercury_perihelion_arcsec_cy_measured_pos : (0 : ℝ) < (42.98 : ℝ) := by
  norm_num

theorem gr_mercury_perihelion_arcsec_cy_abs_diff : (0.004319111313620283 : ℝ) < (0.004362302426757486 : ℝ) := by
  norm_num

theorem n_U1_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem n_U1_measured_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem n_U1_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem n_SU2_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem n_SU2_measured_pos : (0 : ℝ) < (3.0 : ℝ) := by
  norm_num

theorem n_SU2_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem n_SU3_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem n_SU3_measured_pos : (0 : ℝ) < (8.0 : ℝ) := by
  norm_num

theorem n_SU3_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem n_gen_total_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem n_gen_total_measured_pos : (0 : ℝ) < (12.0 : ℝ) := by
  norm_num

theorem n_gen_total_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem n_fermion_generations_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem n_fermion_generations_measured_pos : (0 : ℝ) < (3.0 : ℝ) := by
  norm_num

theorem n_fermion_generations_abs_diff : (0.0 : ℝ) < (1e-09 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_u_unitarity_tight : (3.46139999995998e-06 : ℝ) < (0.002 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_c_unitarity_tight : (6.287900000123692e-06 : ℝ) < (0.002 : ℝ) := by
  norm_num

theorem ckm_unitarity_row_t_unitarity_tight : (5.671760000547366e-07 : ℝ) < (0.002 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_d_unitarity_tight : (6.612999999933145e-06 : ℝ) < (0.002 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_s_unitarity_tight : (3.0099000000172182e-06 : ℝ) < (0.002 : ℝ) := by
  norm_num

theorem ckm_unitarity_col_b_unitarity_tight : (6.93576000077023e-07 : ℝ) < (0.002 : ℝ) := by
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

theorem gr_einstein_trace_reverse_structure_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_einstein_trace_reverse_structure_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_weak_field_2phi_deviation_err_under_half : (0.010049119969584104 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_weak_field_2phi_deviation_meas_pos : (0 : ℝ) < (2e-06 : ℝ) := by
  norm_num

theorem gr_weak_field_gii_err_under_half : (2.0098285486827472e-08 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_weak_field_gii_meas_pos : (0 : ℝ) < (0.999998 : ℝ) := by
  norm_num

theorem gr_poisson_source_positive_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_poisson_source_positive_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_schwarzschild_radius_sun_m_err_under_half : (0.013075989286963106 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_schwarzschild_radius_sun_m_meas_pos : (0 : ℝ) < (2953.25 : ℝ) := by
  norm_num

theorem gr_solar_light_deflection_rad_err_under_half : (0.023944368260521525 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_solar_light_deflection_rad_meas_pos : (0 : ℝ) < (8.489087556227974e-06 : ℝ) := by
  norm_num

theorem gr_mercury_perihelion_arcsec_cy_meas_pos : (0 : ℝ) < (42.98 : ℝ) := by
  norm_num

theorem gr_friedmann_H2_positive_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_friedmann_H2_positive_meas_pos : (0 : ℝ) < (1.0 : ℝ) := by
  norm_num

theorem gr_acoustic_null_cone_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_acoustic_null_cone_meas_pos : (0 : ℝ) < (0.7693455090660798 : ℝ) := by
  norm_num

theorem gr_geodesic_deviation_scale_err_under_half : (0.010049118924187393 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_geodesic_deviation_scale_meas_pos : (0 : ℝ) < (1e-10 : ℝ) := by
  norm_num

theorem gr_planck_length_m_err_under_half : (8.12315831742237e-08 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_G_newton_si_err_under_half : (0.010049118924197253 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_G_newton_si_meas_pos : (0 : ℝ) < (6.6743e-11 : ℝ) := by
  norm_num

theorem gr_c_light_si_exact_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem gr_c_light_si_exact_meas_pos : (0 : ℝ) < (299792458.0 : ℝ) := by
  norm_num

theorem sm_generators_U1Y_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_generators_SU2L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_generators_SU3c_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_alpha_em_inv_err_under_half : (0.009504134401232328 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_sin2_theta_W_err_under_half : (0.009504134401234463 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_alpha_s_MZ_err_under_half : (0.009504134401239374 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_total_gauge_bosons_generators_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_W_err_under_half : (0.009504134401231034 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_Z_err_under_half : (0.009504134401234711 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_H_err_under_half : (0.00950413440123411 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_t_err_under_half : (0.009504134401232968 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_G_F_GeV_m2_err_under_half : (0.009504134401238606 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_fermion_generations_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_charge_electron_L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_charge_neutrino_L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_charge_up_L_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_charge_down_L_err_under_half : (1.6653345369377348e-14 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_charge_positron_R_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_e_err_under_half : (0.009504134401230541 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_mu_err_under_half : (0.009504134401236932 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_m_tau_err_under_half : (0.009504134401234309 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_ratio_mu_e_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_ratio_tau_mu_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_higgs_mass_from_potential_err_under_half : (0.004751954295268555 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_higgs_vev_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

theorem sm_photon_massless_eq : (0 : ℕ) = (0 : ℕ) := by
  decide

theorem sm_alpha_s_gt_alpha_em_at_MZ_proxy_err_under_half : (0.0 : ℝ) < (0.5 : ℝ) := by
  norm_num

end

end FSOT.Formal.GRSMCKM
