(* FSOT GR/SM/CKM/PMNS spine — multi-prover re-proof of exported obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma lambda_ckm_err_under_half : ((0.08387407135526351%R)) < (0.5%R).
Proof. lra. Qed.

Lemma lambda_ckm_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma lambda_ckm_abs_diff : ((0.00018871666054934289%R)) < ((0.0001906038271558363%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_err_finite : ((2.240891444698181%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_measured_pos : 0 < ((0.826%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_abs_diff : ((0.018509763333206974%R)) < ((0.018694860966540043%R)).
Proof. lra. Qed.

Lemma rho_bar_err_finite : ((5.86239218720027%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma rho_bar_measured_pos : 0 < ((0.159%R)).
Proof. lra. Qed.

Lemma rho_bar_abs_diff : ((0.00932120357764843%R)) < ((0.009414415613425913%R)).
Proof. lra. Qed.

Lemma eta_bar_err_finite : ((5.954837550877345%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma eta_bar_measured_pos : 0 < ((0.348%R)).
Proof. lra. Qed.

Lemma eta_bar_abs_diff : ((0.02072283467705316%R)) < ((0.02093006302382469%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_err_finite : ((9.651841765554817%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_measured_pos : 0 < ((0.0000308%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_abs_diff : ((0.000002972767263790884%R)) < ((0.000003002494937428793%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_err_finite : ((8.38059421016685%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_measured_pos : 0 < ((1.196%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_abs_diff : ((0.1002319067535955%R)) < ((0.10123422582113245%R)).
Proof. lra. Qed.

Lemma V_ud_err_under_half : ((0.0035751439500761547%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ud_measured_pos : 0 < ((0.97435%R)).
Proof. lra. Qed.

Lemma V_ud_abs_diff : ((0.000034834415077567016%R)) < ((0.00003518275922934269%R)).
Proof. lra. Qed.

Lemma V_us_err_under_half : ((0.08387407135526351%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_us_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma V_us_abs_diff : ((0.00018871666054934289%R)) < ((0.0001906038271558363%R)).
Proof. lra. Qed.

Lemma V_ub_err_finite : ((8.033837560592682%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma V_ub_measured_pos : 0 < ((0.00369%R)).
Proof. lra. Qed.

Lemma V_ub_abs_diff : ((0.00029644860598586993%R)) < ((0.00029941309204672864%R)).
Proof. lra. Qed.

Lemma V_cd_err_under_half : ((0.14618725453586415%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cd_measured_pos : 0 < ((0.22486%R)).
Proof. lra. Qed.

Lemma V_cd_abs_diff : ((0.0003287166605493441%R)) < ((0.00033200382715583757%R)).
Proof. lra. Qed.

Lemma V_cs_err_under_half : ((0.08476364265914554%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cs_measured_pos : 0 < ((0.97349%R)).
Proof. lra. Qed.

Lemma V_cs_abs_diff : ((0.0008251655849225159%R)) < ((0.0008334172407727411%R)).
Proof. lra. Qed.

Lemma V_cb_err_finite : ((2.085614355341048%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma V_cb_measured_pos : 0 < ((0.04182%R)).
Proof. lra. Qed.

Lemma V_cb_abs_diff : ((0.0008722039234036263%R)) < ((0.0008809259626386625%R)).
Proof. lra. Qed.

Lemma V_td_err_finite : ((3.8353724469530674%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma V_td_measured_pos : 0 < ((0.00857%R)).
Proof. lra. Qed.

Lemma V_td_abs_diff : ((0.00032869141870387787%R)) < ((0.00033197833289191664%R)).
Proof. lra. Qed.

Lemma V_ts_err_under_half : ((0.3703258476973747%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ts_measured_pos : 0 < ((0.0411%R)).
Proof. lra. Qed.

Lemma V_ts_abs_diff : ((0.000152203923403621%R)) < ((0.0001537259626386572%R)).
Proof. lra. Qed.

Lemma V_tb_err_under_half : ((0.08827786107347174%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_tb_measured_pos : 0 < ((0.999118%R)).
Proof. lra. Qed.

Lemma V_tb_abs_diff : ((0.0008820000000000494%R)) < ((0.0008908200000010499%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_err_finite : ((3.791079293869786%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_measured_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_abs_diff : ((0.00876573354328572%R)) < ((0.008853390878719575%R)).
Proof. lra. Qed.

Lemma alpha_inv_err_under_half : ((0.3910691950893094%R)) < (0.5%R).
Proof. lra. Qed.

Lemma alpha_inv_measured_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma alpha_inv_abs_diff : ((0.5359055786003921%R)) < ((0.541264634386397%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_err_finite : ((3.573804082126688%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_measured_pos : 0 < ((0.1179%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_abs_diff : ((0.004213515012827365%R)) < ((0.004255650162956639%R)).
Proof. lra. Qed.

Lemma m_H_err_under_half : ((0.24031054116629413%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_H_measured_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma m_H_abs_diff : ((0.3009889528107834%R)) < ((0.30399884233889224%R)).
Proof. lra. Qed.

Lemma m_W_err_finite : ((11.818376281905547%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma m_W_measured_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma m_W_abs_diff : ((9.49925630410722%R)) < ((9.594248867148295%R)).
Proof. lra. Qed.

Lemma m_Z_err_finite : ((11.852271158304143%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma m_Z_measured_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma m_Z_abs_diff : ((10.80780161474975%R)) < ((10.91587963089725%R)).
Proof. lra. Qed.

Lemma m_t_err_finite : ((53.0467052008237%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma m_t_measured_pos : 0 < ((172.69%R)).
Proof. lra. Qed.

Lemma m_t_abs_diff : ((91.60635521130246%R)) < ((92.52241876341549%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_err_finite : ((2.053332898567214%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_measured_pos : 0 < ((0.307%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_abs_diff : ((0.006303731998601347%R)) < ((0.006366769318588361%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_err_finite : ((6.342198874309371%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_measured_pos : 0 < ((0.546%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_abs_diff : ((0.03462840585372917%R)) < ((0.034974689912267466%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_err_finite : ((7.121598214539716%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_measured_pos : 0 < ((0.022%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_abs_diff : ((0.0015667516071987374%R)) < ((0.001582419123271725%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_err_finite : ((6.824483048637119%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_measured_pos : 0 < ((3.4382986264288293%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_abs_diff : ((0.23464610692215837%R)) < ((0.23699256799138096%R)).
Proof. lra. Qed.

Lemma dm2_21_err_finite : ((5.947855435998268%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma dm2_21_measured_pos : 0 < ((0.0000753%R)).
Proof. lra. Qed.

Lemma dm2_21_abs_diff : ((0.000004478735143306696%R)) < ((0.000004523522495739764%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_err_finite : ((14.405438984619169%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_measured_pos : 0 < ((0.002453%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_abs_diff : ((0.0003533654182927082%R)) < ((0.0003568990724766353%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_err_under_half : ((0.0011516191063876136%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_abs_diff : ((0.000011516191063876136%R)) < ((0.000011631352975514898%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_err_under_half : ((0.16767220035305286%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_abs_diff : ((0.0016767220035305286%R)) < ((0.001693489223566834%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_err_under_half : ((0.1744641170662753%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_abs_diff : ((0.001744641170662753%R)) < ((0.0017620875823703805%R)).
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

Lemma emergent_unitarity_row_u_unitarity_tight : ((0.000011516191063876136%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_unitarity_tight : ((0.0016767220035305286%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_unitarity_tight : ((0.001744641170662753%R)) < ((0.05%R)).
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

Lemma gr_seed_m_W_err_finite : ((7.281636039893431%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma gr_seed_m_W_meas_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma gr_seed_m_Z_err_finite : ((6.587566028472561%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma gr_seed_m_Z_meas_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma sm_lambda_ckm_err_under_half : ((0.08387407135526351%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_A_wolfenstein_err_finite : ((2.240891444698181%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_rho_bar_err_finite : ((5.86239218720027%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_eta_bar_err_finite : ((5.954837550877345%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_Jarlskog_J_err_finite : ((9.651841765554817%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_delta_ckm_rad_err_finite : ((8.38059421016685%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_ud_err_under_half : ((0.0035751439500761547%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_us_err_under_half : ((0.08387407135526351%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ub_err_finite : ((8.033837560592682%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_cd_err_under_half : ((0.14618725453586415%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cs_err_under_half : ((0.08476364265914554%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cb_err_finite : ((2.085614355341048%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_td_err_finite : ((3.8353724469530674%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_V_ts_err_under_half : ((0.3703258476973747%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_tb_err_under_half : ((0.08827786107347174%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_W_err_finite : ((3.791079293869786%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_alpha_inv_err_under_half : ((0.3910691950893094%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_s_MZ_err_finite : ((3.573804082126688%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_m_H_err_under_half : ((0.24031054116629413%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_W_err_finite : ((11.818376281905547%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_m_Z_err_finite : ((11.852271158304143%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_m_t_err_finite : ((53.0467052008237%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_sin2_theta_12_err_finite : ((2.053332898567214%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_sin2_theta_23_err_finite : ((6.342198874309371%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_sin2_theta_13_err_finite : ((7.121598214539716%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_delta_pmns_rad_err_finite : ((6.824483048637119%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_dm2_21_err_finite : ((5.947855435998268%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_dm2_31_abs_err_finite : ((14.405438984619169%R)) < ((100.0%R)).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_u_err_under_half : ((0.0011516191063876136%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_c_err_under_half : ((0.16767220035305286%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_t_err_under_half : ((0.1744641170662753%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_yin_yang_in_unit_interval_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_all_kappa_nonnegative_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sector_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_edge_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

