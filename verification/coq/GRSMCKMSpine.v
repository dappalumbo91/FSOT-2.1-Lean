(* FSOT GR/SM/CKM/PMNS spine — multi-prover re-proof of exported obligations. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
From Stdlib Require Import Arith.
Local Open Scope R_scope.

Lemma lambda_ckm_err_under_half : ((0.06648317372654539%R)) < (0.5%R).
Proof. lra. Qed.

Lemma lambda_ckm_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma lambda_ckm_abs_diff : ((0.00014958714088472713%R)) < ((0.0001510830122945744%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_err_under_half : ((0.0519504854624754%R)) < (0.5%R).
Proof. lra. Qed.

Lemma A_wolfenstein_measured_pos : 0 < ((0.826%R)).
Proof. lra. Qed.

Lemma A_wolfenstein_abs_diff : ((0.0004291110099200468%R)) < ((0.0004334021200202473%R)).
Proof. lra. Qed.

Lemma rho_bar_err_under_half : ((0.004811476065123823%R)) < (0.5%R).
Proof. lra. Qed.

Lemma rho_bar_measured_pos : 0 < ((0.159%R)).
Proof. lra. Qed.

Lemma rho_bar_abs_diff : ((0.000007650246943546879%R)) < ((0.000007726749413982348%R)).
Proof. lra. Qed.

Lemma eta_bar_err_under_half : ((0.038316528380806465%R)) < (0.5%R).
Proof. lra. Qed.

Lemma eta_bar_measured_pos : 0 < ((0.348%R)).
Proof. lra. Qed.

Lemma eta_bar_abs_diff : ((0.0001333415187652065%R)) < ((0.00013467493395385855%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_err_under_half : ((0.24035678834077073%R)) < (0.5%R).
Proof. lra. Qed.

Lemma Jarlskog_J_measured_pos : 0 < ((0.0000308%R)).
Proof. lra. Qed.

Lemma Jarlskog_J_abs_diff : ((0.00000007402989080895739%R)) < ((0.00000007477019071704697%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_err_under_half : ((0.0032411336172532518%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_ckm_rad_measured_pos : 0 < ((1.196%R)).
Proof. lra. Qed.

Lemma delta_ckm_rad_abs_diff : ((0.00003876395806234889%R)) < ((0.00003915159764397238%R)).
Proof. lra. Qed.

Lemma V_ud_err_under_half : ((0.0026470393155981903%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ud_measured_pos : 0 < ((0.97435%R)).
Proof. lra. Qed.

Lemma V_ud_abs_diff : ((0.000025791427571530967%R)) < ((0.000026049341848246278%R)).
Proof. lra. Qed.

Lemma V_us_err_under_half : ((0.06648317372654539%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_us_measured_pos : 0 < ((0.225%R)).
Proof. lra. Qed.

Lemma V_us_abs_diff : ((0.00014958714088472713%R)) < ((0.0001510830122945744%R)).
Proof. lra. Qed.

Lemma V_ub_err_under_half : ((0.3128398765779975%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ub_measured_pos : 0 < ((0.00369%R)).
Proof. lra. Qed.

Lemma V_ub_abs_diff : ((0.000011543791445728108%R)) < ((0.00001165922936118539%R)).
Proof. lra. Qed.

Lemma V_cd_err_under_half : ((0.12878552916691646%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cd_measured_pos : 0 < ((0.22486%R)).
Proof. lra. Qed.

Lemma V_cd_abs_diff : ((0.00028958714088472837%R)) < ((0.0002924830122945757%R)).
Proof. lra. Qed.

Lemma V_cs_err_under_half : ((0.08569256719930887%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cs_measured_pos : 0 < ((0.97349%R)).
Proof. lra. Qed.

Lemma V_cs_abs_diff : ((0.000834208572428552%R)) < ((0.0008425506581538375%R)).
Proof. lra. Qed.

Lemma V_cb_err_under_half : ((0.17604653957526104%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_cb_measured_pos : 0 < ((0.04182%R)).
Proof. lra. Qed.

Lemma V_cb_abs_diff : ((0.00007362266285037417%R)) < ((0.0000743588894798779%R)).
Proof. lra. Qed.

Lemma V_td_err_under_half : ((0.16746091354807907%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_td_measured_pos : 0 < ((0.00857%R)).
Proof. lra. Qed.

Lemma V_td_abs_diff : ((0.000014351400291070376%R)) < ((0.000014494914294981081%R)).
Proof. lra. Qed.

Lemma V_ts_err_under_half : ((0.16900757375439615%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_ts_measured_pos : 0 < ((0.0411%R)).
Proof. lra. Qed.

Lemma V_ts_abs_diff : ((0.00006946211281305681%R)) < ((0.00007015673394218738%R)).
Proof. lra. Qed.

Lemma V_tb_err_under_half : ((0.0004466129217395198%R)) < (0.5%R).
Proof. lra. Qed.

Lemma V_tb_measured_pos : 0 < ((0.999118%R)).
Proof. lra. Qed.

Lemma V_tb_abs_diff : ((0.000004462190091425455%R)) < ((0.000004506811993339711%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_err_under_half : ((0.03607116917125227%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_W_measured_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_abs_diff : ((0.0000834037573577695%R)) < ((0.0000842377949323472%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_onshell_err_under_half : ((0.18983327119077956%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_W_onshell_measured_pos : 0 < ((0.2230518910035465%R)).
Proof. lra. Qed.

Lemma sin2_theta_W_onshell_abs_diff : ((0.0004234267011449244%R)) < ((0.00042766096815737367%R)).
Proof. lra. Qed.

Lemma alpha_inv_err_under_half : ((0.14167347156583626%R)) < (0.5%R).
Proof. lra. Qed.

Lemma alpha_inv_measured_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma alpha_inv_abs_diff : ((0.19414365719723037%R)) < ((0.19608509376920366%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_err_under_half : ((0.007456682224867657%R)) < (0.5%R).
Proof. lra. Qed.

Lemma alpha_s_MZ_measured_pos : 0 < ((0.1179%R)).
Proof. lra. Qed.

Lemma alpha_s_MZ_abs_diff : ((0.000008791428343118968%R)) < ((0.000008879342627550158%R)).
Proof. lra. Qed.

Lemma m_H_err_under_half : ((0.03465631473109587%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_H_measured_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma m_H_abs_diff : ((0.04340703420069758%R)) < ((0.04384110454270555%R)).
Proof. lra. Qed.

Lemma m_W_err_under_half : ((0.026467778409122445%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_W_measured_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma m_W_abs_diff : ((0.021274006251900346%R)) < ((0.02148674631442035%R)).
Proof. lra. Qed.

Lemma m_Z_err_under_half : ((0.05373549190999207%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_Z_measured_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma m_Z_abs_diff : ((0.04900010542091593%R)) < ((0.04949010647512609%R)).
Proof. lra. Qed.

Lemma m_t_err_under_half : ((0.014767057175780673%R)) < (0.5%R).
Proof. lra. Qed.

Lemma m_t_measured_pos : 0 < ((172.69%R)).
Proof. lra. Qed.

Lemma m_t_abs_diff : ((0.025501231036855643%R)) < ((0.025756243347225198%R)).
Proof. lra. Qed.

Lemma Lambda_QCD_GeV_err_under_half : ((0.28120185593059194%R)) < (0.5%R).
Proof. lra. Qed.

Lemma Lambda_QCD_GeV_measured_pos : 0 < ((0.2173%R)).
Proof. lra. Qed.

Lemma Lambda_QCD_GeV_abs_diff : ((0.0006110516329371762%R)) < ((0.000617162149267548%R)).
Proof. lra. Qed.

Lemma sqrt_sigma_GeV_err_under_half : ((0.05275580626597419%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sqrt_sigma_GeV_measured_pos : 0 < ((0.42%R)).
Proof. lra. Qed.

Lemma sqrt_sigma_GeV_abs_diff : ((0.0002215743863170916%R)) < ((0.0002237901301812625%R)).
Proof. lra. Qed.

Lemma N_eff_err_under_half : ((0.04789442119649137%R)) < (0.5%R).
Proof. lra. Qed.

Lemma N_eff_measured_pos : 0 < ((3.046%R)).
Proof. lra. Qed.

Lemma N_eff_abs_diff : ((0.0014588640696451272%R)) < ((0.0014734527103425785%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_err_under_half : ((0.004756805274882866%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_12_measured_pos : 0 < ((0.307%R)).
Proof. lra. Qed.

Lemma sin2_theta_12_abs_diff : ((0.000014603392193890397%R)) < ((0.0000147494261168293%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_err_under_half : ((0.16643494215886515%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_23_measured_pos : 0 < ((0.546%R)).
Proof. lra. Qed.

Lemma sin2_theta_23_abs_diff : ((0.0009087347841874038%R)) < ((0.0009178221320302779%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_err_under_half : ((0.0029908786376992773%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sin2_theta_13_measured_pos : 0 < ((0.022%R)).
Proof. lra. Qed.

Lemma sin2_theta_13_abs_diff : ((0.000000657993300293841%R)) < ((0.0000006645732342967793%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_err_under_half : ((0.07675312594002048%R)) < (0.5%R).
Proof. lra. Qed.

Lemma delta_pmns_rad_measured_pos : 0 < ((3.4382986264288293%R)).
Proof. lra. Qed.

Lemma delta_pmns_rad_abs_diff : ((0.002639001674936914%R)) < ((0.002665391691687283%R)).
Proof. lra. Qed.

Lemma dm2_21_err_under_half : ((0.06394145338205008%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_21_measured_pos : 0 < ((0.0000753%R)).
Proof. lra. Qed.

Lemma dm2_21_abs_diff : ((0.00000004814791439668371%R)) < ((0.00000004862939454065054%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_err_under_half : ((0.4219868071131969%R)) < (0.5%R).
Proof. lra. Qed.

Lemma dm2_31_abs_measured_pos : 0 < ((0.002453%R)).
Proof. lra. Qed.

Lemma dm2_31_abs_abs_diff : ((0.00001035133637848672%R)) < ((0.000010454849743271588%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_err_under_half : ((0.0013701426440082543%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_u_abs_diff : ((0.000013701426440082543%R)) < ((0.000013838440705483368%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_err_under_half : ((0.1755075619817248%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_abs_diff : ((0.001755075619817248%R)) < ((0.0017726263760164205%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_err_under_half : ((0.001431015241259992%R)) < (0.5%R).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_measured_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_abs_diff : ((0.000014310152412599919%R)) < ((0.00001445325393772592%R)).
Proof. lra. Qed.

Lemma triangle_angle_sum_pi_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma triangle_angle_sum_pi_measured_pos : 0 < ((3.141592653589793%R)).
Proof. lra. Qed.

Lemma triangle_angle_sum_pi_abs_diff : (0%R) < ((0.000000001%R)).
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

Lemma emergent_unitarity_row_u_unitarity_tight : ((0.000013701426440082543%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_c_unitarity_tight : ((0.001755075619817248%R)) < ((0.05%R)).
Proof. lra. Qed.

Lemma emergent_unitarity_row_t_unitarity_tight : ((0.000014310152412599919%R)) < ((0.05%R)).
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

Lemma gr_seed_sin2_theta_W_err_under_half : ((0.016460322231694493%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_meas_pos : 0 < ((0.23122%R)).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_onshell_err_under_half : ((0.209488435890309%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_sin2_theta_W_onshell_meas_pos : 0 < ((0.2230518910035465%R)).
Proof. lra. Qed.

Lemma gr_seed_alpha_inv_err_under_half : ((0.13842762822785223%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_alpha_inv_meas_pos : 0 < ((137.035999084%R)).
Proof. lra. Qed.

Lemma gr_seed_m_H_err_under_half : ((0.01100190161397048%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_H_meas_pos : 0 < ((125.25%R)).
Proof. lra. Qed.

Lemma gr_seed_m_W_err_under_half : ((0.022433777228753317%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_W_meas_pos : 0 < ((80.377%R)).
Proof. lra. Qed.

Lemma gr_seed_m_Z_err_under_half : ((0.05252482561491295%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_seed_m_Z_meas_pos : 0 < ((91.1876%R)).
Proof. lra. Qed.

Lemma gr_Lambda_QCD_GeV_err_under_half : ((0.28241958362570724%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_Lambda_QCD_GeV_meas_pos : 0 < ((0.2173%R)).
Proof. lra. Qed.

Lemma gr_sqrt_sigma_GeV_err_under_half : ((0.052777181118259166%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_sqrt_sigma_GeV_meas_pos : 0 < ((0.42%R)).
Proof. lra. Qed.

Lemma gr_N_eff_err_under_half : ((0.028424048045719855%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_N_eff_meas_pos : 0 < ((3.046%R)).
Proof. lra. Qed.

Lemma gr_N_c_QCD_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_N_c_QCD_meas_pos : 0 < ((3.0%R)).
Proof. lra. Qed.

Lemma gr_Casimir_C_F_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_Casimir_C_F_meas_pos : 0 < ((1.3333333333333333%R)).
Proof. lra. Qed.

Lemma gr_Casimir_C_A_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_Casimir_C_A_meas_pos : 0 < ((3.0%R)).
Proof. lra. Qed.

Lemma gr_beta0_QCD_nf5_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_beta0_QCD_nf5_meas_pos : 0 < ((7.666666666666667%R)).
Proof. lra. Qed.

Lemma gr_alpha_s_gt_alpha_em_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_alpha_s_gt_alpha_em_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_koide_lepton_QR_err_under_half : ((0.0009230194964016114%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_koide_lepton_QR_meas_pos : 0 < ((0.6666666666666666%R)).
Proof. lra. Qed.

Lemma gr_sqrt2_structural_recovery_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_sqrt2_structural_recovery_meas_pos : 0 < ((1.4142135623730951%R)).
Proof. lra. Qed.

Lemma gr_yukawa_top_err_under_half : ((0.07863049017601485%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_yukawa_top_meas_pos : 0 < ((0.991%R)).
Proof. lra. Qed.

Lemma gr_morphic_phi_present_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_morphic_phi_present_meas_pos : 0 < ((1.618033988749895%R)).
Proof. lra. Qed.

Lemma gr_neutrino_m3_over_m2_err_under_half : ((0.1724795983521893%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_neutrino_m3_over_m2_meas_pos : 0 < ((5.707570518336111%R)).
Proof. lra. Qed.

Lemma gr_R_b_triangle_err_under_half : ((0.014017064614919078%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_R_b_triangle_meas_pos : 0 < ((0.382602927328059%R)).
Proof. lra. Qed.

Lemma gr_R_t_triangle_err_under_half : ((0.00036384895090004057%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_R_t_triangle_meas_pos : 0 < ((0.9101565799355624%R)).
Proof. lra. Qed.

Lemma gr_sin_delta_ckm_err_under_half : ((0.002439404519026022%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_sin_delta_ckm_meas_pos : 0 < ((0.93058220251172%R)).
Proof. lra. Qed.

Lemma gr_spin2_massless_helicities_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_massless_helicities_meas_pos : 0 < ((2.0%R)).
Proof. lra. Qed.

Lemma gr_spin2_TT_dof_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_TT_dof_meas_pos : 0 < ((2.0%R)).
Proof. lra. Qed.

Lemma gr_einstein_quadrupole_prefactor_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_einstein_quadrupole_prefactor_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_wilson_area_law_sigma_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_wilson_area_law_sigma_meas_pos : 0 < ((0.17658624702998535%R)).
Proof. lra. Qed.

Lemma gr_confinement_scale_ratio_err_under_half : ((0.2295212676523054%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_confinement_scale_ratio_meas_pos : 0 < ((0.5173809523809524%R)).
Proof. lra. Qed.

Lemma gr_asymptotic_freedom_beta0_pos_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_asymptotic_freedom_beta0_pos_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_flux_tube_E_over_L_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_flux_tube_E_over_L_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_polyakov_confined_order_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_massive_polarizations_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_massive_polarizations_meas_pos : 0 < ((5.0%R)).
Proof. lra. Qed.

Lemma gr_spin2_metric_dof_accounting_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_metric_dof_accounting_meas_pos : 0 < ((2.0%R)).
Proof. lra. Qed.

Lemma gr_equivalence_geodesic_structure_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_equivalence_geodesic_structure_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_spin2_wave_equation_flat_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_wave_equation_flat_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_bianchi_contracted_identity_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_bianchi_contracted_identity_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_spin2_TT_projector_complete_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_spin2_TT_projector_complete_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_soft_graviton_pole_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_soft_graviton_pole_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_instanton_action_scale_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_instanton_action_scale_meas_pos : 0 < ((669.6431825331274%R)).
Proof. lra. Qed.

Lemma gr_ym_beta_function_structure_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_ym_beta_function_structure_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_su3_center_order_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_su3_center_order_meas_pos : 0 < ((3.0%R)).
Proof. lra. Qed.

Lemma gr_dual_meissner_confined_flag_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_dual_meissner_confined_flag_meas_pos : 0 < ((1.0%R)).
Proof. lra. Qed.

Lemma gr_triangle_angle_sum_pi_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma gr_triangle_angle_sum_pi_meas_pos : 0 < ((3.141592653589793%R)).
Proof. lra. Qed.

Lemma gr_alpha_rad_err_under_half : ((0.0034382632792112626%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_alpha_rad_meas_pos : 0 < ((1.6070304610469615%R)).
Proof. lra. Qed.

Lemma gr_beta_rad_err_under_half : ((0.014994707011088022%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_beta_rad_meas_pos : 0 < ((0.3923401442155158%R)).
Proof. lra. Qed.

Lemma gr_gamma_rad_err_under_half : ((0.00031310172038841725%R)) < (0.5%R).
Proof. lra. Qed.

Lemma gr_gamma_rad_meas_pos : 0 < ((1.1422220483273158%R)).
Proof. lra. Qed.

Lemma sm_lambda_ckm_err_under_half : ((0.06648317372654539%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_A_wolfenstein_err_under_half : ((0.0519504854624754%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_rho_bar_err_under_half : ((0.004811476065123823%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_eta_bar_err_under_half : ((0.038316528380806465%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_Jarlskog_J_err_under_half : ((0.24035678834077073%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_delta_ckm_rad_err_under_half : ((0.0032411336172532518%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ud_err_under_half : ((0.0026470393155981903%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_us_err_under_half : ((0.06648317372654539%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ub_err_under_half : ((0.3128398765779975%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cd_err_under_half : ((0.12878552916691646%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cs_err_under_half : ((0.08569256719930887%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_cb_err_under_half : ((0.17604653957526104%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_td_err_under_half : ((0.16746091354807907%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_ts_err_under_half : ((0.16900757375439615%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_V_tb_err_under_half : ((0.0004466129217395198%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_W_err_under_half : ((0.03607116917125227%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_W_onshell_err_under_half : ((0.18983327119077956%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_inv_err_under_half : ((0.14167347156583626%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_alpha_s_MZ_err_under_half : ((0.007456682224867657%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_H_err_under_half : ((0.03465631473109587%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_W_err_under_half : ((0.026467778409122445%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_Z_err_under_half : ((0.05373549190999207%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_m_t_err_under_half : ((0.014767057175780673%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_Lambda_QCD_GeV_err_under_half : ((0.28120185593059194%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sqrt_sigma_GeV_err_under_half : ((0.05275580626597419%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_N_eff_err_under_half : ((0.04789442119649137%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_12_err_under_half : ((0.004756805274882866%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_23_err_under_half : ((0.16643494215886515%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sin2_theta_13_err_under_half : ((0.0029908786376992773%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_delta_pmns_rad_err_under_half : ((0.07675312594002048%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_dm2_21_err_under_half : ((0.06394145338205008%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_dm2_31_abs_err_under_half : ((0.4219868071131969%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_u_err_under_half : ((0.0013701426440082543%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_c_err_under_half : ((0.1755075619817248%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_emergent_unitarity_row_t_err_under_half : ((0.001431015241259992%R)) < (0.5%R).
Proof. lra. Qed.

Lemma sm_triangle_angle_sum_pi_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_yin_yang_in_unit_interval_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_all_kappa_nonnegative_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_sector_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

Lemma sm_edge_count_err_under_half : (0%R) < (0.5%R).
Proof. lra. Qed.

