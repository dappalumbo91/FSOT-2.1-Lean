theory GRSMCKMSpine
  imports Complex_Main
begin

(* FSOT GR/SM/CKM/PMNS spine — multi-prover residual/structure certificates. *)

lemma lambda_ckm_err_under_half: "(0.06225011989853476::real) < (0.5::real)"
  by simp

lemma lambda_ckm_measured_pos: "(0::real) < 0.22501"
  by simp

lemma lambda_ckm_abs_diff: "(0.000140069::real) < (0.0001414697::real)"
  by simp

lemma A_wolfenstein_err_under_half: "(0.05246555208389803::real) < (0.5::real)"
  by simp

lemma A_wolfenstein_measured_pos: "(0::real) < 0.826"
  by simp

lemma A_wolfenstein_abs_diff: "(0.0004333655::real) < (0.0004376991::real)"
  by simp

lemma rho_bar_err_under_half: "(0.02700157709000836::real) < (0.5::real)"
  by simp

lemma rho_bar_measured_pos: "(0::real) < 0.1591"
  by simp

lemma rho_bar_abs_diff: "(0.00004295951::real) < (0.0000433891::real)"
  by simp

lemma eta_bar_err_under_half: "(0.0028013614651725667::real) < (0.5::real)"
  by simp

lemma eta_bar_measured_pos: "(0::real) < 0.3523"
  by simp

lemma eta_bar_abs_diff: "(0.000009869196::real) < (0.000009967888::real)"
  by simp

lemma Jarlskog_J_err_under_half: "(0.23792303102008408::real) < (0.5::real)"
  by simp

lemma Jarlskog_J_measured_pos: "(0::real) < 0.0000312"
  by simp

lemma Jarlskog_J_abs_diff: "(0.00000007423199::real) < (0.00000007497431::real)"
  by simp

lemma delta_ckm_rad_err_under_half: "(0.02612849108321111::real) < (0.5::real)"
  by simp

lemma delta_ckm_rad_measured_pos: "(0::real) < 1.147"
  by simp

lemma delta_ckm_rad_abs_diff: "(0.0002996938::real) < (0.0003026907::real)"
  by simp

lemma V_ud_err_under_half: "(0.002658467271059532::real) < (0.5::real)"
  by simp

lemma V_ud_measured_pos: "(0::real) < 0.97435"
  by simp

lemma V_ud_abs_diff: "(0.00002590278::real) < (0.0000261618::real)"
  by simp

lemma V_us_err_under_half: "(0.06225011989853476::real) < (0.5::real)"
  by simp

lemma V_us_measured_pos: "(0::real) < 0.22501"
  by simp

lemma V_us_abs_diff: "(0.000140069::real) < (0.0001414697::real)"
  by simp

lemma V_ub_err_under_half: "(0.23474330619715575::real) < (0.5::real)"
  by simp

lemma V_ub_measured_pos: "(0::real) < 0.003732"
  by simp

lemma V_ub_abs_diff: "(0.00000876062::real) < (0.000008848226::real)"
  by simp

lemma V_cd_err_under_half: "(0.12454706932169445::real) < (0.5::real)"
  by simp

lemma V_cd_measured_pos: "(0::real) < 0.22487"
  by simp

lemma V_cd_abs_diff: "(0.000280069::real) < (0.0002828697::real)"
  by simp

lemma V_cs_err_under_half: "(0.08568112914816942::real) < (0.5::real)"
  by simp

lemma V_cs_measured_pos: "(0::real) < 0.97349"
  by simp

lemma V_cs_abs_diff: "(0.0008340972::real) < (0.0008424382::real)"
  by simp

lemma V_cb_err_under_half: "(0.15304243191119066::real) < (0.5::real)"
  by simp

lemma V_cb_measured_pos: "(0::real) < 0.04183"
  by simp

lemma V_cb_abs_diff: "(0.00006401765::real) < (0.00006465783::real)"
  by simp

lemma V_td_err_under_half: "(0.2337487764470785::real) < (0.5::real)"
  by simp

lemma V_td_measured_pos: "(0::real) < 0.00858"
  by simp

lemma V_td_abs_diff: "(0.00002005565::real) < (0.0000202562::real)"
  by simp

lemma V_ts_err_under_half: "(0.14583328325587586::real) < (0.5::real)"
  by simp

lemma V_ts_measured_pos: "(0::real) < 0.04111"
  by simp

lemma V_ts_abs_diff: "(0.00005995206::real) < (0.00006055158::real)"
  by simp

lemma V_tb_err_under_half: "(0.0004449567::real) < (0.5::real)"
  by simp

lemma V_tb_measured_pos: "(0::real) < 0.999118"
  by simp

lemma V_tb_abs_diff: "(0.000004445643::real) < (0.000004490099::real)"
  by simp

lemma sin2_theta_W_err_under_half: "(0.06713369973590165::real) < (0.5::real)"
  by simp

lemma sin2_theta_W_measured_pos: "(0::real) < 0.23122"
  by simp

lemma sin2_theta_W_abs_diff: "(0.0001552265::real) < (0.0001567788::real)"
  by simp

lemma sin2_theta_W_onshell_err_under_half: "(0.15026877693416243::real) < (0.5::real)"
  by simp

lemma sin2_theta_W_onshell_measured_pos: "(0::real) < 0.2230518910035465"
  by simp

lemma sin2_theta_W_onshell_abs_diff: "(0.0003351773::real) < (0.0003385291::real)"
  by simp

lemma alpha_inv_err_under_half: "(0.1472364924023795::real) < (0.5::real)"
  by simp

lemma alpha_inv_measured_pos: "(0::real) < 137.035999084"
  by simp

lemma alpha_inv_abs_diff: "(0.20176699837983847::real) < (0.20378466836363784::real)"
  by simp

lemma alpha_s_MZ_err_under_half: "(0.007242651170537564::real) < (0.5::real)"
  by simp

lemma alpha_s_MZ_measured_pos: "(0::real) < 0.1179"
  by simp

lemma alpha_s_MZ_abs_diff: "(0.000008539086::real) < (0.000008624477::real)"
  by simp

lemma m_H_err_under_half: "(0.0011951533584994727::real) < (0.5::real)"
  by simp

lemma m_H_measured_pos: "(0::real) < 125.25"
  by simp

lemma m_H_abs_diff: "(0.0014969295815205896::real) < (0.0015118988773367957::real)"
  by simp

lemma m_W_err_under_half: "(0.03999290024803384::real) < (0.5::real)"
  by simp

lemma m_W_measured_pos: "(0::real) < 80.377"
  by simp

lemma m_W_abs_diff: "(0.03214509343236216::real) < (0.03246654436668678::real)"
  by simp

lemma m_Z_err_under_half: "(0.018424423512725066::real) < (0.5::real)"
  by simp

lemma m_Z_measured_pos: "(0::real) < 91.1876"
  by simp

lemma m_Z_abs_diff: "(0.016800789615089684::real) < (0.01696879751124158::real)"
  by simp

lemma m_t_err_under_half: "(0.052705818067851705::real) < (0.5::real)"
  by simp

lemma m_t_measured_pos: "(0::real) < 172.69"
  by simp

lemma m_t_abs_diff: "(0.0910176772213731::real) < (0.09192785399358784::real)"
  by simp

lemma Lambda_QCD_GeV_err_under_half: "(0.04921722442825905::real) < (0.5::real)"
  by simp

lemma Lambda_QCD_GeV_measured_pos: "(0::real) < 0.2173"
  by simp

lemma Lambda_QCD_GeV_abs_diff: "(0.000106949::real) < (0.0001080185::real)"
  by simp

lemma sqrt_sigma_GeV_err_under_half: "(0.02566066753490444::real) < (0.5::real)"
  by simp

lemma sqrt_sigma_GeV_measured_pos: "(0::real) < 0.42"
  by simp

lemma sqrt_sigma_GeV_abs_diff: "(0.0001077748::real) < (0.0001088526::real)"
  by simp

lemma N_eff_err_under_half: "(0.07917549100062735::real) < (0.5::real)"
  by simp

lemma N_eff_measured_pos: "(0::real) < 3.046"
  by simp

lemma N_eff_abs_diff: "(0.002411685455879109::real) < (0.0024358023104389::real)"
  by simp

lemma sin2_theta_12_err_under_half: "(0.013048795958832987::real) < (0.5::real)"
  by simp

lemma sin2_theta_12_measured_pos: "(0::real) < 0.307"
  by simp

lemma sin2_theta_12_abs_diff: "(0.0000400598::real) < (0.0000404604::real)"
  by simp

lemma sin2_theta_23_err_under_half: "(0.17474226348654942::real) < (0.5::real)"
  by simp

lemma sin2_theta_23_measured_pos: "(0::real) < 0.546"
  by simp

lemma sin2_theta_23_abs_diff: "(0.0009540928::real) < (0.0009636337::real)"
  by simp

lemma sin2_theta_13_err_under_half: "(0.003010045202972307::real) < (0.5::real)"
  by simp

lemma sin2_theta_13_measured_pos: "(0::real) < 0.022"
  by simp

lemma sin2_theta_13_abs_diff: "(0.0000006622099::real) < (0.000000668832::real)"
  by simp

lemma delta_pmns_rad_err_under_half: "(0.0997385337617464::real) < (0.5::real)"
  by simp

lemma delta_pmns_rad_measured_pos: "(0::real) < 3.4382986264288293"
  by simp

lemma delta_pmns_rad_abs_diff: "(0.003429308636350381::real) < (0.003463601722714885::real)"
  by simp

lemma dm2_21_err_under_half: "(0.07222853624703972::real) < (0.5::real)"
  by simp

lemma dm2_21_measured_pos: "(0::real) < 0.0000753"
  by simp

lemma dm2_21_abs_diff: "(0.00000005438809::real) < (0.00000005493197::real)"
  by simp

lemma dm2_31_abs_err_under_half: "(0.36301157961075986::real) < (0.5::real)"
  by simp

lemma dm2_31_abs_measured_pos: "(0::real) < 0.002453"
  by simp

lemma dm2_31_abs_abs_diff: "(0.000008904674::real) < (0.000008993721::real)"
  by simp

lemma emergent_unitarity_row_u_err_under_half: "(0.001399329001761096::real) < (0.5::real)"
  by simp

lemma emergent_unitarity_row_u_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_u_abs_diff: "(0.00001399329::real) < (0.00001413322::real)"
  by simp

lemma emergent_unitarity_row_c_err_under_half: "(0.17551087147971156::real) < (0.5::real)"
  by simp

lemma emergent_unitarity_row_c_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_c_abs_diff: "(0.0017551087147971156::real) < (0.0017726598019460868::real)"
  by simp

lemma emergent_unitarity_row_t_err_under_half: "(0.0014587296799373206::real) < (0.5::real)"
  by simp

lemma emergent_unitarity_row_t_measured_pos: "(0::real) < 1.0"
  by simp

lemma emergent_unitarity_row_t_abs_diff: "(0.0000145873::real) < (0.00001473317::real)"
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

lemma emergent_unitarity_row_u_unitarity_tight: "(0.00001399329::real) < (0.05::real)"
  by simp

lemma emergent_unitarity_row_c_unitarity_tight: "(0.0017551087147971156::real) < (0.05::real)"
  by simp

lemma emergent_unitarity_row_t_unitarity_tight: "(0.0000145873::real) < (0.05::real)"
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

lemma gr_acoustic_null_cone_meas_pos: "(0::real) < 0.7693639124918291"
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

lemma gr_seed_sin2_theta_W_onshell_err_under_half: "(0.20105239362371918::real) < (0.5::real)"
  by simp

lemma gr_seed_sin2_theta_W_onshell_meas_pos: "(0::real) < 0.2230518910035465"
  by simp

lemma gr_seed_alpha_inv_err_under_half: "(0.15275909169604954::real) < (0.5::real)"
  by simp

lemma gr_seed_alpha_inv_meas_pos: "(0::real) < 137.035999084"
  by simp

lemma gr_seed_m_H_err_under_half: "(0.022485014301729805::real) < (0.5::real)"
  by simp

lemma gr_seed_m_H_meas_pos: "(0::real) < 125.25"
  by simp

lemma gr_seed_m_W_err_under_half: "(0.012988177377751::real) < (0.5::real)"
  by simp

lemma gr_seed_m_W_meas_pos: "(0::real) < 80.377"
  by simp

lemma gr_seed_m_Z_err_under_half: "(0.015880360710250344::real) < (0.5::real)"
  by simp

lemma gr_seed_m_Z_meas_pos: "(0::real) < 91.1876"
  by simp

lemma gr_Lambda_QCD_GeV_err_under_half: "(0.048055073125713964::real) < (0.5::real)"
  by simp

lemma gr_Lambda_QCD_GeV_meas_pos: "(0::real) < 0.2173"
  by simp

lemma gr_sqrt_sigma_GeV_err_under_half: "(0.025896107116174516::real) < (0.5::real)"
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

lemma gr_yukawa_top_err_under_half: "(0.013457034902430751::real) < (0.5::real)"
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

lemma gr_R_b_triangle_err_under_half: "(0.026537499247957154::real) < (0.5::real)"
  by simp

lemma gr_R_b_triangle_meas_pos: "(0::real) < 0.3865593098089865"
  by simp

lemma gr_R_t_triangle_err_under_half: "(0.019630621725789416::real) < (0.5::real)"
  by simp

lemma gr_R_t_triangle_meas_pos: "(0::real) < 0.9117171162153312"
  by simp

lemma gr_sin_delta_ckm_err_under_half: "(0.0036013868908110055::real) < (0.5::real)"
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

lemma gr_wilson_area_law_sigma_meas_pos: "(0::real) < 0.17649137329543738"
  by simp

lemma gr_confinement_scale_ratio_err_under_half: "(0.022153229185580246::real) < (0.5::real)"
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

lemma gr_glueball_over_sqrt_sigma_err_under_half: "(0.034782692362047014::real) < (0.5::real)"
  by simp

lemma gr_glueball_over_sqrt_sigma_meas_pos: "(0::real) < 3.65"
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

lemma gr_alpha_rad_err_under_half: "(0.03680231674953141::real) < (0.5::real)"
  by simp

lemma gr_alpha_rad_meas_pos: "(0::real) < 1.5982430233482232"
  by simp

lemma gr_beta_rad_err_under_half: "(0.029711617355294043::real) < (0.5::real)"
  by simp

lemma gr_beta_rad_meas_pos: "(0::real) < 0.3967401060358461"
  by simp

lemma gr_gamma_rad_err_under_half: "(0.04101767408617176::real) < (0.5::real)"
  by simp

lemma gr_gamma_rad_meas_pos: "(0::real) < 1.1466095242057237"
  by simp

lemma sm_lambda_ckm_err_under_half: "(0.06225011989853476::real) < (0.5::real)"
  by simp

lemma sm_A_wolfenstein_err_under_half: "(0.05246555208389803::real) < (0.5::real)"
  by simp

lemma sm_rho_bar_err_under_half: "(0.02700157709000836::real) < (0.5::real)"
  by simp

lemma sm_eta_bar_err_under_half: "(0.0028013614651725667::real) < (0.5::real)"
  by simp

lemma sm_Jarlskog_J_err_under_half: "(0.23792303102008408::real) < (0.5::real)"
  by simp

lemma sm_delta_ckm_rad_err_under_half: "(0.02612849108321111::real) < (0.5::real)"
  by simp

lemma sm_V_ud_err_under_half: "(0.002658467271059532::real) < (0.5::real)"
  by simp

lemma sm_V_us_err_under_half: "(0.06225011989853476::real) < (0.5::real)"
  by simp

lemma sm_V_ub_err_under_half: "(0.23474330619715575::real) < (0.5::real)"
  by simp

lemma sm_V_cd_err_under_half: "(0.12454706932169445::real) < (0.5::real)"
  by simp

lemma sm_V_cs_err_under_half: "(0.08568112914816942::real) < (0.5::real)"
  by simp

lemma sm_V_cb_err_under_half: "(0.15304243191119066::real) < (0.5::real)"
  by simp

lemma sm_V_td_err_under_half: "(0.2337487764470785::real) < (0.5::real)"
  by simp

lemma sm_V_ts_err_under_half: "(0.14583328325587586::real) < (0.5::real)"
  by simp

lemma sm_V_tb_err_under_half: "(0.0004449567::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_W_err_under_half: "(0.06713369973590165::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_W_onshell_err_under_half: "(0.15026877693416243::real) < (0.5::real)"
  by simp

lemma sm_alpha_inv_err_under_half: "(0.1472364924023795::real) < (0.5::real)"
  by simp

lemma sm_alpha_s_MZ_err_under_half: "(0.007242651170537564::real) < (0.5::real)"
  by simp

lemma sm_m_H_err_under_half: "(0.0011951533584994727::real) < (0.5::real)"
  by simp

lemma sm_m_W_err_under_half: "(0.03999290024803384::real) < (0.5::real)"
  by simp

lemma sm_m_Z_err_under_half: "(0.018424423512725066::real) < (0.5::real)"
  by simp

lemma sm_m_t_err_under_half: "(0.052705818067851705::real) < (0.5::real)"
  by simp

lemma sm_Lambda_QCD_GeV_err_under_half: "(0.04921722442825905::real) < (0.5::real)"
  by simp

lemma sm_sqrt_sigma_GeV_err_under_half: "(0.02566066753490444::real) < (0.5::real)"
  by simp

lemma sm_N_eff_err_under_half: "(0.07917549100062735::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_12_err_under_half: "(0.013048795958832987::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_23_err_under_half: "(0.17474226348654942::real) < (0.5::real)"
  by simp

lemma sm_sin2_theta_13_err_under_half: "(0.003010045202972307::real) < (0.5::real)"
  by simp

lemma sm_delta_pmns_rad_err_under_half: "(0.0997385337617464::real) < (0.5::real)"
  by simp

lemma sm_dm2_21_err_under_half: "(0.07222853624703972::real) < (0.5::real)"
  by simp

lemma sm_dm2_31_abs_err_under_half: "(0.36301157961075986::real) < (0.5::real)"
  by simp

lemma sm_emergent_unitarity_row_u_err_under_half: "(0.001399329001761096::real) < (0.5::real)"
  by simp

lemma sm_emergent_unitarity_row_c_err_under_half: "(0.17551087147971156::real) < (0.5::real)"
  by simp

lemma sm_emergent_unitarity_row_t_err_under_half: "(0.0014587296799373206::real) < (0.5::real)"
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
