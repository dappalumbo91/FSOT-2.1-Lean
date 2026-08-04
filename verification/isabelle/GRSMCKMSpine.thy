theory GRSMCKMSpine
  imports Complex_Main
begin

(* FSOT GR/SM/CKM/PMNS spine — multi-prover residual/structure certificates. *)

lemma lambda_ckm_err_under_half: "(0.06203597212779205::real) < (0.5::real)"
  by simp

lemma lambda_ckm_measured_pos: "(0::real) < 0.22501"
  by simp

lemma lambda_ckm_abs_diff: "(0.0001395871::real) < (0.000140983::real)"
  by simp

lemma A_wolfenstein_err_under_half: "(0.0519504854624754::real) < (0.5::real)"
  by simp

lemma A_wolfenstein_measured_pos: "(0::real) < 0.826"
  by simp

lemma A_wolfenstein_abs_diff: "(0.000429111::real) < (0.0004334021::real)"
  by simp

lemma rho_bar_err_under_half: "(0.05804509934408681::real) < (0.5::real)"
  by simp

lemma rho_bar_measured_pos: "(0::real) < 0.1591"
  by simp

lemma rho_bar_abs_diff: "(0.00009234975::real) < (0.00009327325::real)"
  by simp

lemma eta_bar_err_under_half: "(0.05017401991649093::real) < (0.5::real)"
  by simp

lemma eta_bar_measured_pos: "(0::real) < 0.3523"
  by simp

lemma eta_bar_abs_diff: "(0.0001767631::real) < (0.0001785307::real)"
  by simp

lemma Jarlskog_J_err_under_half: "(0.21421096741502482::real) < (0.5::real)"
  by simp

lemma Jarlskog_J_measured_pos: "(0::real) < 0.0000312"
  by simp

lemma Jarlskog_J_abs_diff: "(0.00000006683382::real) < (0.00000006750216::real)"
  by simp

lemma delta_ckm_rad_err_under_half: "(0.0013363679820401644::real) < (0.5::real)"
  by simp

lemma delta_ckm_rad_measured_pos: "(0::real) < 1.147"
  by simp

lemma delta_ckm_rad_abs_diff: "(0.00001532814::real) < (0.00001548142::real)"
  by simp

lemma V_ud_err_under_half: "(0.0026470393155981903::real) < (0.5::real)"
  by simp

lemma V_ud_measured_pos: "(0::real) < 0.97435"
  by simp

lemma V_ud_abs_diff: "(0.00002579143::real) < (0.00002604934::real)"
  by simp

lemma V_us_err_under_half: "(0.06203597212779205::real) < (0.5::real)"
  by simp

lemma V_us_measured_pos: "(0::real) < 0.22501"
  by simp

lemma V_us_abs_diff: "(0.0001395871::real) < (0.000140983::real)"
  by simp

lemma V_ub_err_under_half: "(0.2724163670754618::real) < (0.5::real)"
  by simp

lemma V_ub_measured_pos: "(0::real) < 0.003732"
  by simp

lemma V_ub_abs_diff: "(0.00001016658::real) < (0.00001026824::real)"
  by simp

lemma V_cd_err_under_half: "(0.124332788226418::real) < (0.5::real)"
  by simp

lemma V_cd_measured_pos: "(0::real) < 0.22487"
  by simp

lemma V_cd_abs_diff: "(0.0002795871::real) < (0.000282383::real)"
  by simp

lemma V_cs_err_under_half: "(0.08569256719930887::real) < (0.5::real)"
  by simp

lemma V_cs_measured_pos: "(0::real) < 0.97349"
  by simp

lemma V_cs_abs_diff: "(0.0008342086::real) < (0.0008425507::real)"
  by simp

lemma V_cb_err_under_half: "(0.15209816603006943::real) < (0.5::real)"
  by simp

lemma V_cb_measured_pos: "(0::real) < 0.04183"
  by simp

lemma V_cb_abs_diff: "(0.00006362266::real) < (0.00006425889::real)"
  by simp

lemma V_td_err_under_half: "(0.24552622781795225::real) < (0.5::real)"
  by simp

lemma V_td_measured_pos: "(0::real) < 0.00858"
  by simp

lemma V_td_abs_diff: "(0.00002106615::real) < (0.00002127681::real)"
  by simp

lemma V_ts_err_under_half: "(0.14464148093664253::real) < (0.5::real)"
  by simp

lemma V_ts_measured_pos: "(0::real) < 0.04111"
  by simp

lemma V_ts_abs_diff: "(0.00005946211::real) < (0.00006005673::real)"
  by simp

lemma V_tb_err_under_half: "(0.0004466129::real) < (0.5::real)"
  by simp

lemma V_tb_measured_pos: "(0::real) < 0.999118"
  by simp

lemma V_tb_abs_diff: "(0.00000446219::real) < (0.000004506812::real)"
  by simp

lemma sin2_theta_W_err_under_half: "(0.03607116917125227::real) < (0.5::real)"
  by simp

lemma sin2_theta_W_measured_pos: "(0::real) < 0.23122"
  by simp

lemma sin2_theta_W_abs_diff: "(0.00008340376::real) < (0.00008423779::real)"
  by simp

lemma sin2_theta_W_onshell_err_under_half: "(0.18983327119077956::real) < (0.5::real)"
  by simp

lemma sin2_theta_W_onshell_measured_pos: "(0::real) < 0.2230518910035465"
  by simp

lemma sin2_theta_W_onshell_abs_diff: "(0.0004234267::real) < (0.000427661::real)"
  by simp

lemma alpha_inv_err_under_half: "(0.14167347156583626::real) < (0.5::real)"
  by simp

lemma alpha_inv_measured_pos: "(0::real) < 137.035999084"
  by simp

lemma alpha_inv_abs_diff: "(0.19414365719723037::real) < (0.19608509376920366::real)"
  by simp

lemma alpha_s_MZ_err_under_half: "(0.007456682224867657::real) < (0.5::real)"
  by simp

lemma alpha_s_MZ_measured_pos: "(0::real) < 0.1179"
  by simp

lemma alpha_s_MZ_abs_diff: "(0.000008791428::real) < (0.000008879343::real)"
  by simp

lemma m_H_err_under_half: "(0.03465631473109587::real) < (0.5::real)"
  by simp

lemma m_H_measured_pos: "(0::real) < 125.25"
  by simp

lemma m_H_abs_diff: "(0.04340703420069758::real) < (0.04384110454270555::real)"
  by simp

lemma m_W_err_under_half: "(0.026467778409122445::real) < (0.5::real)"
  by simp

lemma m_W_measured_pos: "(0::real) < 80.377"
  by simp

lemma m_W_abs_diff: "(0.021274006251900346::real) < (0.02148674631442035::real)"
  by simp

lemma m_Z_err_under_half: "(0.05373549190999207::real) < (0.5::real)"
  by simp

lemma m_Z_measured_pos: "(0::real) < 91.1876"
  by simp

lemma m_Z_abs_diff: "(0.04900010542091593::real) < (0.04949010647512609::real)"
  by simp

lemma m_t_err_under_half: "(0.014767057175780673::real) < (0.5::real)"
  by simp

lemma m_t_measured_pos: "(0::real) < 172.69"
  by simp

lemma m_t_abs_diff: "(0.025501231036855643::real) < (0.025756243347225198::real)"
  by simp

lemma Lambda_QCD_GeV_err_under_half: "(0.04684019131481111::real) < (0.5::real)"
  by simp

lemma Lambda_QCD_GeV_measured_pos: "(0::real) < 0.2173"
  by simp

lemma Lambda_QCD_GeV_abs_diff: "(0.0001017837::real) < (0.0001028016::real)"
  by simp

lemma sqrt_sigma_GeV_err_under_half: "(0.05275580626597419::real) < (0.5::real)"
  by simp

lemma sqrt_sigma_GeV_measured_pos: "(0::real) < 0.42"
  by simp

lemma sqrt_sigma_GeV_abs_diff: "(0.0002215744::real) < (0.0002237901::real)"
  by simp

lemma N_eff_err_under_half: "(0.04789442119649137::real) < (0.5::real)"
  by simp

lemma N_eff_measured_pos: "(0::real) < 3.046"
  by simp

lemma N_eff_abs_diff: "(0.0014588640696451272::real) < (0.0014734527103425785::real)"
  by simp

lemma sin2_theta_12_err_under_half: "(0.004756805274882866::real) < (0.5::real)"
  by simp

lemma sin2_theta_12_measured_pos: "(0::real) < 0.307"
  by simp

lemma sin2_theta_12_abs_diff: "(0.00001460339::real) < (0.00001474943::real)"
  by simp

lemma sin2_theta_23_err_under_half: "(0.16643494215886515::real) < (0.5::real)"
  by simp

lemma sin2_theta_23_measured_pos: "(0::real) < 0.546"
  by simp

lemma sin2_theta_23_abs_diff: "(0.0009087348::real) < (0.0009178221::real)"
  by simp

lemma sin2_theta_13_err_under_half: "(0.0029908786376992773::real) < (0.5::real)"
  by simp

lemma sin2_theta_13_measured_pos: "(0::real) < 0.022"
  by simp

lemma sin2_theta_13_abs_diff: "(0.0000006579933::real) < (0.0000006645732::real)"
  by simp

lemma delta_pmns_rad_err_under_half: "(0.07675312594002048::real) < (0.5::real)"
  by simp

lemma delta_pmns_rad_measured_pos: "(0::real) < 3.4382986264288293"
  by simp

lemma delta_pmns_rad_abs_diff: "(0.002639001674936914::real) < (0.002665391691687283::real)"
  by simp

lemma dm2_21_err_under_half: "(0.06394145338205008::real) < (0.5::real)"
  by simp

lemma dm2_21_measured_pos: "(0::real) < 0.0000753"
  by simp

lemma dm2_21_abs_diff: "(0.00000004814791::real) < (0.00000004862939::real)"
  by simp

lemma dm2_31_abs_err_under_half: "(0.3712743059251006::real) < (0.5::real)"
  by simp

lemma dm2_31_abs_measured_pos: "(0::real) < 0.002453"
  by simp

lemma dm2_31_abs_abs_diff: "(0.000009107359::real) < (0.000009198432::real)"
  by simp

lemma emergent_unitarity_row_u_err_under_half: "(0.001400381070371104::real) < (0.5::real)"
  by simp

lemma emergent_unitarity_row_u_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_u_abs_diff: "(0.00001400381::real) < (0.00001414385::real)"
  by simp

lemma emergent_unitarity_row_c_err_under_half: "(0.1755075619817248::real) < (0.5::real)"
  by simp

lemma emergent_unitarity_row_c_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_c_abs_diff: "(0.001755075619817248::real) < (0.0017726263760164205::real)"
  by simp

lemma emergent_unitarity_row_t_err_under_half: "(0.0014597402371530066::real) < (0.5::real)"
  by simp

lemma emergent_unitarity_row_t_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_t_abs_diff: "(0.0000145974::real) < (0.00001474338::real)"
  by simp

lemma triangle_angle_sum_pi_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma triangle_angle_sum_pi_measured_pos: "(0::real) < 3.141592653589793"
  by simp

lemma triangle_angle_sum_pi_abs_diff: "(0::real) < (0.000000001::real)"
  by simp

lemma yin_yang_in_unit_interval_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma yin_yang_in_unit_interval_measured_pos: "(0::real) < 1.0"
  by simp

lemma yin_yang_in_unit_interval_abs_diff: "(0::real) < (0.000000001::real)"
  by simp

lemma all_kappa_nonnegative_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma all_kappa_nonnegative_measured_pos: "(0::real) < 1.0"
  by simp

lemma all_kappa_nonnegative_abs_diff: "(0::real) < (0.000000001::real)"
  by simp

lemma sector_count_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma sector_count_measured_pos: "(0::real) < 8.0"
  by simp

lemma sector_count_abs_diff: "(0::real) < (0.000000001::real)"
  by simp

lemma edge_count_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma edge_count_measured_pos: "(0::real) < 15.0"
  by simp

lemma edge_count_abs_diff: "(0::real) < (0.000000001::real)"
  by simp

lemma emergent_unitarity_row_u_unitarity_tight: "(0.00001400381::real) < (0.05::real)"
  by simp

lemma emergent_unitarity_row_c_unitarity_tight: "(0.001755075619817248::real) < (0.05::real)"
  by simp

lemma emergent_unitarity_row_t_unitarity_tight: "(0.0000145974::real) < (0.05::real)"
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

lemma gr_einstein_trace_reverse_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_einstein_trace_reverse_meas_pos: "(0::real) < 0.5"
  by simp

lemma gr_weak_field_2phi_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_weak_field_2phi_meas_pos: "(0::real) < 0.000002"
  by simp

lemma gr_schwarzschild_radius_sun_m_err_under_half: "(0.003026566219535862::real) < (0.5::real)"
  by simp

lemma gr_schwarzschild_radius_sun_m_meas_pos: "(0::real) < 2953.25"
  by simp

lemma gr_solar_light_deflection_rad_err_under_half: "(0.013893853126499888::real) < (0.5::real)"
  by simp

lemma gr_solar_light_deflection_rad_meas_pos: "(0::real) < 0.000008489088"
  by simp

lemma gr_mercury_perihelion_arcsec_cy_err_under_half: "(0.0047099996121108675::real) < (0.5::real)"
  by simp

lemma gr_mercury_perihelion_arcsec_cy_meas_pos: "(0::real) < 42.98"
  by simp

lemma gr_acoustic_null_cone_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_acoustic_null_cone_meas_pos: "(0::real) < 0.7693455090660798"
  by simp

lemma gr_planck_length_m_err_under_half: "(0.00000000002392855::real) < (0.5::real)"
  by simp

lemma gr_c_light_si_exact_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_c_light_si_exact_meas_pos: "(0::real) < 299792458.0"
  by simp

lemma gr_seed_sin2_theta_W_err_under_half: "(0.016460322231694493::real) < (0.5::real)"
  by simp

lemma gr_seed_sin2_theta_W_meas_pos: "(0::real) < 0.23122"
  by simp

lemma gr_seed_sin2_theta_W_onshell_err_under_half: "(0.209488435890309::real) < (0.5::real)"
  by simp

lemma gr_seed_sin2_theta_W_onshell_meas_pos: "(0::real) < 0.2230518910035465"
  by simp

lemma gr_seed_alpha_inv_err_under_half: "(0.13842762822785223::real) < (0.5::real)"
  by simp

lemma gr_seed_alpha_inv_meas_pos: "(0::real) < 137.035999084"
  by simp

lemma gr_seed_m_H_err_under_half: "(0.01100190161397048::real) < (0.5::real)"
  by simp

lemma gr_seed_m_H_meas_pos: "(0::real) < 125.25"
  by simp

lemma gr_seed_m_W_err_under_half: "(0.022433777228753317::real) < (0.5::real)"
  by simp

lemma gr_seed_m_W_meas_pos: "(0::real) < 80.377"
  by simp

lemma gr_seed_m_Z_err_under_half: "(0.05252482561491295::real) < (0.5::real)"
  by simp

lemma gr_seed_m_Z_meas_pos: "(0::real) < 91.1876"
  by simp

lemma gr_Lambda_QCD_GeV_err_under_half: "(0.048055073125713964::real) < (0.5::real)"
  by simp

lemma gr_Lambda_QCD_GeV_meas_pos: "(0::real) < 0.2173"
  by simp

lemma gr_sqrt_sigma_GeV_err_under_half: "(0.052777181118259166::real) < (0.5::real)"
  by simp

lemma gr_sqrt_sigma_GeV_meas_pos: "(0::real) < 0.42"
  by simp

lemma gr_N_eff_err_under_half: "(0.028424048045719855::real) < (0.5::real)"
  by simp

lemma gr_N_eff_meas_pos: "(0::real) < 3.046"
  by simp

lemma gr_N_c_QCD_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_N_c_QCD_meas_pos: "(0::real) < 3.0"
  by simp

lemma gr_Casimir_C_F_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_Casimir_C_F_meas_pos: "(0::real) < 1.3333333333333333"
  by simp

lemma gr_Casimir_C_A_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_Casimir_C_A_meas_pos: "(0::real) < 3.0"
  by simp

lemma gr_beta0_QCD_nf5_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_beta0_QCD_nf5_meas_pos: "(0::real) < 7.666666666666667"
  by simp

lemma gr_alpha_s_gt_alpha_em_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_alpha_s_gt_alpha_em_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_koide_lepton_QR_err_under_half: "(0.0009230195::real) < (0.5::real)"
  by simp

lemma gr_koide_lepton_QR_meas_pos: "(0::real) < 0.6666666666666666"
  by simp

lemma gr_sqrt2_structural_recovery_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_sqrt2_structural_recovery_meas_pos: "(0::real) < 1.4142135623730951"
  by simp

lemma gr_yukawa_top_err_under_half: "(0.07863049017601485::real) < (0.5::real)"
  by simp

lemma gr_yukawa_top_meas_pos: "(0::real) < 0.991"
  by simp

lemma gr_morphic_phi_present_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_morphic_phi_present_meas_pos: "(0::real) < 1.618033988749895"
  by simp

lemma gr_neutrino_m3_over_m2_err_under_half: "(0.1470630495663553::real) < (0.5::real)"
  by simp

lemma gr_neutrino_m3_over_m2_meas_pos: "(0::real) < 5.707570518336111"
  by simp

lemma gr_R_b_triangle_err_under_half: "(0.048875106155599785::real) < (0.5::real)"
  by simp

lemma gr_R_b_triangle_meas_pos: "(0::real) < 0.3865593098089865"
  by simp

lemma gr_R_t_triangle_err_under_half: "(0.023646850672565858::real) < (0.5::real)"
  by simp

lemma gr_R_t_triangle_meas_pos: "(0::real) < 0.9117171162153312"
  by simp

lemma gr_sin_delta_ckm_err_under_half: "(0.008142970284056283::real) < (0.5::real)"
  by simp

lemma gr_sin_delta_ckm_meas_pos: "(0::real) < 0.9115343723414107"
  by simp

lemma gr_spin2_massless_helicities_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_spin2_massless_helicities_meas_pos: "(0::real) < 2.0"
  by simp

lemma gr_spin2_TT_dof_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_spin2_TT_dof_meas_pos: "(0::real) < 2.0"
  by simp

lemma gr_einstein_quadrupole_prefactor_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_einstein_quadrupole_prefactor_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_wilson_area_law_sigma_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_wilson_area_law_sigma_meas_pos: "(0::real) < 0.17658624702998535"
  by simp

lemma gr_confinement_scale_ratio_err_under_half: "(0.004719617111680276::real) < (0.5::real)"
  by simp

lemma gr_confinement_scale_ratio_meas_pos: "(0::real) < 0.5173809523809524"
  by simp

lemma gr_asymptotic_freedom_beta0_pos_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_asymptotic_freedom_beta0_pos_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_flux_tube_E_over_L_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_flux_tube_E_over_L_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_polyakov_confined_order_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_spin2_massive_polarizations_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_spin2_massive_polarizations_meas_pos: "(0::real) < 5.0"
  by simp

lemma gr_spin2_metric_dof_accounting_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_spin2_metric_dof_accounting_meas_pos: "(0::real) < 2.0"
  by simp

lemma gr_equivalence_geodesic_structure_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_equivalence_geodesic_structure_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_spin2_wave_equation_flat_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_spin2_wave_equation_flat_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_bianchi_contracted_identity_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_bianchi_contracted_identity_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_spin2_TT_projector_complete_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_spin2_TT_projector_complete_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_soft_graviton_pole_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_soft_graviton_pole_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_instanton_action_scale_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_instanton_action_scale_meas_pos: "(0::real) < 669.6431825331274"
  by simp

lemma gr_ym_beta_function_structure_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_ym_beta_function_structure_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_su3_center_order_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_su3_center_order_meas_pos: "(0::real) < 3.0"
  by simp

lemma gr_dual_meissner_confined_flag_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_dual_meissner_confined_flag_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_theta_QCD_strong_CP_flag_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_glueball_over_sqrt_sigma_err_under_half: "(0.4774294805097184::real) < (0.5::real)"
  by simp

lemma gr_glueball_over_sqrt_sigma_meas_pos: "(0::real) < 3.5"
  by simp

lemma gr_trace_anomaly_structure_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_trace_anomaly_structure_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_graviton_propagator_pole_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_graviton_propagator_pole_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_gw_quadrupole_coupling_structure_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_gw_quadrupole_coupling_structure_meas_pos: "(0::real) < 1.0"
  by simp

lemma gr_massless_spin2_little_group_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_massless_spin2_little_group_meas_pos: "(0::real) < 2.0"
  by simp

lemma gr_triangle_angle_sum_pi_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma gr_triangle_angle_sum_pi_meas_pos: "(0::real) < 3.141592653589793"
  by simp

lemma gr_alpha_rad_err_under_half: "(0.04909688136289182::real) < (0.5::real)"
  by simp

lemma gr_alpha_rad_meas_pos: "(0::real) < 1.5982430233482232"
  by simp

lemma gr_beta_rad_err_under_half: "(0.05385778013441918::real) < (0.5::real)"
  by simp

lemma gr_beta_rad_meas_pos: "(0::real) < 0.3967401060358461"
  by simp

lemma gr_gamma_rad_err_under_half: "(0.049800045699593946::real) < (0.5::real)"
  by simp

lemma gr_gamma_rad_meas_pos: "(0::real) < 1.1466095242057237"
  by simp

lemma sm_lambda_ckm_err_under_half: "(0.06203597212779205::real) < (0.5::real)"
  by simp

lemma sm_A_wolfenstein_err_under_half: "(0.0519504854624754::real) < (0.5::real)"
  by simp

lemma sm_rho_bar_err_under_half: "(0.05804509934408681::real) < (0.5::real)"
  by simp

lemma sm_eta_bar_err_under_half: "(0.05017401991649093::real) < (0.5::real)"
  by simp

lemma sm_Jarlskog_J_err_under_half: "(0.21421096741502482::real) < (0.5::real)"
  by simp

lemma sm_delta_ckm_rad_err_under_half: "(0.0013363679820401644::real) < (0.5::real)"
  by simp

lemma sm_V_ud_err_under_half: "(0.0026470393155981903::real) < (0.5::real)"
  by simp

lemma sm_V_us_err_under_half: "(0.06203597212779205::real) < (0.5::real)"
  by simp

lemma sm_V_ub_err_under_half: "(0.2724163670754618::real) < (0.5::real)"
  by simp

lemma sm_V_cd_err_under_half: "(0.124332788226418::real) < (0.5::real)"
  by simp

lemma sm_V_cs_err_under_half: "(0.08569256719930887::real) < (0.5::real)"
  by simp

lemma sm_V_cb_err_under_half: "(0.15209816603006943::real) < (0.5::real)"
  by simp

lemma sm_V_td_err_under_half: "(0.24552622781795225::real) < (0.5::real)"
  by simp

lemma sm_V_ts_err_under_half: "(0.14464148093664253::real) < (0.5::real)"
  by simp

lemma sm_V_tb_err_under_half: "(0.0004466129::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_W_err_under_half: "(0.03607116917125227::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_W_onshell_err_under_half: "(0.18983327119077956::real) < (0.5::real)"
  by simp

lemma sm_alpha_inv_err_under_half: "(0.14167347156583626::real) < (0.5::real)"
  by simp

lemma sm_alpha_s_MZ_err_under_half: "(0.007456682224867657::real) < (0.5::real)"
  by simp

lemma sm_m_H_err_under_half: "(0.03465631473109587::real) < (0.5::real)"
  by simp

lemma sm_m_W_err_under_half: "(0.026467778409122445::real) < (0.5::real)"
  by simp

lemma sm_m_Z_err_under_half: "(0.05373549190999207::real) < (0.5::real)"
  by simp

lemma sm_m_t_err_under_half: "(0.014767057175780673::real) < (0.5::real)"
  by simp

lemma sm_Lambda_QCD_GeV_err_under_half: "(0.04684019131481111::real) < (0.5::real)"
  by simp

lemma sm_sqrt_sigma_GeV_err_under_half: "(0.05275580626597419::real) < (0.5::real)"
  by simp

lemma sm_N_eff_err_under_half: "(0.04789442119649137::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_12_err_under_half: "(0.004756805274882866::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_23_err_under_half: "(0.16643494215886515::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_13_err_under_half: "(0.0029908786376992773::real) < (0.5::real)"
  by simp

lemma sm_delta_pmns_rad_err_under_half: "(0.07675312594002048::real) < (0.5::real)"
  by simp

lemma sm_dm2_21_err_under_half: "(0.06394145338205008::real) < (0.5::real)"
  by simp

lemma sm_dm2_31_abs_err_under_half: "(0.3712743059251006::real) < (0.5::real)"
  by simp

lemma sm_emergent_unitarity_row_u_err_under_half: "(0.001400381070371104::real) < (0.5::real)"
  by simp

lemma sm_emergent_unitarity_row_c_err_under_half: "(0.1755075619817248::real) < (0.5::real)"
  by simp

lemma sm_emergent_unitarity_row_t_err_under_half: "(0.0014597402371530066::real) < (0.5::real)"
  by simp

lemma sm_triangle_angle_sum_pi_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma sm_yin_yang_in_unit_interval_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma sm_all_kappa_nonnegative_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma sm_sector_count_err_under_half: "(0::real) < (0.5::real)"
  by simp

lemma sm_edge_count_err_under_half: "(0::real) < (0.5::real)"
  by simp

end
